// Obtener referencias a elementos HTML
const nodeCountInput = document.getElementById("nodeCount");
const createNodesButton = document.getElementById("createNodes");
const nodeNamesDiv = document.getElementById("nodeNames");
const connectionFromSelect = document.getElementById("connectionFrom");
const connectionToSelect = document.getElementById("connectionTo");
const connectNodesButton = document.getElementById("connectNodes");
const consultButton = document.getElementById("consulta");

// Datos para almacenar nodos y conexiones
let nodes = [];
let connections = [];
let oldConections = [];

// Crear el lienzo SVG
const svgWidth = 1344;
const svgHeight = 688;
const svg = d3
  .select("#graph")
  .attr("width", svgWidth)
  .attr("Height", svgHeight);

// Calcular el centro en función del tamaño actual
const centerX = svgWidth / 2;
const centerY = svgHeight / 2;
console.log(centerX, centerY);
// Crear el simulador de fuerzas para el grafo
const simulation = d3
  .forceSimulation()
  .force(
    "link",
    d3.forceLink().id((d) => d.id)
  )
  .force("charge", d3.forceManyBody().strength(-600))
  .force("center", d3.forceCenter(centerX, centerY));

// Función para crear nodos
createNodesButton.addEventListener("click", () => {
  const count = parseInt(nodeCountInput.value);

  if (!isNaN(count)) {
    nodes = [];
    nodeNamesDiv.innerHTML = "";

    for (let i = 0; i < count; i++) {
      const nodeName = prompt(`Nombre del Nodo ${i + 1}:`);
      nodes.push({ id: i, name: nodeName });
      nodeNamesDiv.innerHTML += `Nodo ${i + 1}: ${nodeName}<br>`;
    }

    updateConnectionSelects();
    updateGraph();
  }
});

// Función para conectar nodos
connectNodesButton.addEventListener("click", () => {
  const fromNodeId = parseInt(connectionFromSelect.value);
  const toNodeId = parseInt(connectionToSelect.value);

  if (!isNaN(fromNodeId) && !isNaN(toNodeId)) {
    const weight = prompt(
      `Peso de la conexión entre Nodo ${fromNodeId} y Nodo ${toNodeId}:`
    );
    if (!isNaN(weight)) {
      connections.push({
        source: fromNodeId,
        target: toNodeId,
        weight: parseInt(weight),
      });
      console.log(connections);
      updateGraph();
    } else {
      alert("Ingrese un peso válido.");
    }
  }
});

// Actualizar opciones de selección para las conexiones
function updateConnectionSelects() {
  connectionFromSelect.innerHTML = "";
  connectionToSelect.innerHTML = "";

  for (let i = 0; i < nodes.length; i++) {
    connectionFromSelect.innerHTML += `<option value="${i}">${nodes[i].name}</option>`;
    connectionToSelect.innerHTML += `<option value="${i}">${nodes[i].name}</option>`;
  }
}

// Actualizar el grafo
function updateGraph() {
  // Actualizar los nodos
  const nodeElements = svg
    .selectAll(".node")
    .data(nodes, (d) => d.id)
    .enter()
    .append("circle")
    .attr("class", "node")
    .attr("r", 15)
    .attr("fill", "blue")
    .call(
      d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    );

  nodeElements.exit().remove();

  // Actualizar las conexiones
  const linkElements = svg
    .selectAll(".link")
    .data(connections)
    .enter()
    .append("line")
    .attr("class", "link")
    .attr("stroke", "gray")
    .attr("stroke-width", (d) => d.weight);

  linkElements.exit().remove();

  const nodeLabels = svg
    .selectAll(".node-label")
    .data(nodes, (d) => d.id)
    .enter()
    .append("text")
    .attr("class", "node-label")
    .attr("text-anchor", "middle")
    .attr("fill", "white") // Centra horizontalmente el texto en el nodo
    .text((d) => d.name);

  nodeLabels.exit().remove();

  const linkLabels = svg
    .selectAll(".link-label")
    .data(connections)
    .enter()
    .append("text")
    .attr("class", "link-label")
    .attr("text-anchor", "middle")
    .attr("fill", "black")
    .text((d) => `Peso: ${d.weight}`);

  // Vincular datos al simulador de fuerzas
  simulation.nodes(nodes).on("tick", ticked);
  simulation.force("link").links(connections);

  linkElements
    .merge(linkElements)
    .attr("x1", (d) => nodes[d.source.id].x)
    .attr("y1", (d) => nodes[d.source.id].y)
    .attr("x2", (d) => nodes[d.target.id].x)
    .attr("y2", (d) => nodes[d.target.id].y);
}

// Funciones para el arrastre de nodos
function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

// Función para actualizar la posición de los nodos y conexiones en el lienzo SVG
function ticked() {
  const offsetX = centerX - d3.mean(nodes, (d) => d.x);
  const offsetY = centerY - d3.mean(nodes, (d) => d.y);

  svg
    .selectAll(".node")
    .attr("cx", (d) => d.x + offsetX)
    .attr("cy", (d) => d.y + offsetY);

  svg
    .selectAll(".link")
    .attr("x1", (d) => d.source.x + offsetX)
    .attr("y1", (d) => d.source.y + offsetY)
    .attr("x2", (d) => d.target.x + offsetX)
    .attr("y2", (d) => d.target.y + offsetY);

  svg
    .selectAll(".node-label")
    .attr("dx", (d) => d.x)
    .attr("dy", (d) => d.y);
}
// Llama a la función de creación inicial de nodos
createNodesButton.click();

function groupConnectedNodes(connections) {
  const groups = [];

  connections.forEach((connection) => {
    const sourceId = connection.source.id;
    const targetId = connection.target.id;

    // Buscar si el nodo ya está en algún grupo
    const groupIndex = groups.findIndex(
      (group) => group.sig.includes(sourceId) || group.sig.includes(targetId)
    );

    if (groupIndex === -1) {
      // Si no se encuentra en ningún grupo, crear un nuevo grupo
      groups.push({ sig: [sourceId, targetId], peso: {} });
    } else {
      // Si ya está en un grupo, agregarlo a ese grupo
      groups[groupIndex].sig.push(sourceId, targetId);
    }
  });

  return groups;
}

consultButton.addEventListener("click", () => {
  console.log(groupConnectedNodes(connections));
});
//Esta función groupConnectedNodes recorre las conexiones y agrupa los nodos que están conectados en un objeto que cumple con el formato que mencionaste. En este ejemplo, groupedNodes contendrá los grupos de nodos conectados.
