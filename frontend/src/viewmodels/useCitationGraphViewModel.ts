import { useCallback, useEffect, useRef } from "react";
import type { Core, EventObject } from "cytoscape";
import type { GraphNode, GraphResponse } from "../models/Graph";

export function useCitationGraphViewModel(
  graph: GraphResponse,
  onSelectNode: (node: GraphNode | null) => void,
  onError: (message: string) => void,
) {
  const containerRef = useRef<HTMLDivElement>(null);
  const graphRef = useRef<Core | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    let disposed = false;
    let instance: Core | null = null;

    void import("cytoscape")
      .then(({ default: createCytoscape }) => {
        if (disposed || !containerRef.current) return;

        const nodesById = new Map(graph.nodes.map((node) => [node.id, node]));
        instance = createCytoscape({
          container: containerRef.current,
          elements: [
            ...graph.nodes.map((node) => ({
              data: {
                id: node.id,
                label: node.title,
                isMatch: node.is_match,
                citations: node.citations_received,
                hasMetadata: node.paper_id !== null,
              },
            })),
            ...graph.edges.map((edge, index) => ({
              data: { id: `edge-${index}`, source: edge.source, target: edge.target },
            })),
          ],
          style: [
            {
              selector: "node",
              style: {
                label: "data(label)",
                "text-wrap": "wrap",
                "text-max-width": "108px",
                "font-size": "10px",
                color: "#35445b",
                "text-valign": "bottom",
                "text-margin-y": 8,
                "text-background-color": "#ffffff",
                "text-background-opacity": 0.88,
                "text-background-padding": "2px",
                width: "mapData(citations, 0, 100, 25, 48)",
                height: "mapData(citations, 0, 100, 25, 48)",
                "background-color": "#6d83a4",
                "border-width": 2,
                "border-color": "#ffffff",
                "overlay-opacity": 0,
              },
            },
            {
              selector: "node[?isMatch]",
              style: {
                "background-color": "#275dad",
                "border-color": "#bdd4ff",
                "border-width": 4,
                "font-weight": 700,
              },
            },
            {
              selector: "node[!hasMetadata]",
              style: { "background-color": "#c3cad5", "border-color": "#ffffff" },
            },
            {
              selector: "edge",
              style: {
                width: 1.5,
                "line-color": "#aebcd0",
                "target-arrow-color": "#8fa1ba",
                "target-arrow-shape": "triangle",
                "curve-style": "bezier",
                "arrow-scale": 0.9,
                opacity: 0.8,
              },
            },
            {
              selector: "node:selected",
              style: { "border-color": "#f0a332", "border-width": 5 },
            },
          ],
          layout: {
            name: "cose",
            animate: false,
            nodeRepulsion: () => 4800,
            idealEdgeLength: () => 115,
            padding: 40,
          },
          minZoom: 0.25,
          maxZoom: 2.5,
        });

        instance.on("tap", "node", (event: EventObject) => {
          onSelectNode(nodesById.get(event.target.id()) ?? null);
        });
        instance.on("tap", (event: EventObject) => {
          if (instance && event.target === instance) onSelectNode(null);
        });
        graphRef.current = instance;
      })
      .catch(() => {
        if (!disposed) {
          onError("Não foi possível carregar a visualização do grafo. Recarregue a página.");
        }
      });

    return () => {
      disposed = true;
      if (instance) {
        instance.destroy();
        if (graphRef.current === instance) graphRef.current = null;
      }
    };
  }, [graph, onError, onSelectNode]);

  const zoom = useCallback((factor: number) => {
    const cy = graphRef.current;
    if (!cy) return;
    cy.zoom({
      level: Math.min(cy.maxZoom(), Math.max(cy.minZoom(), cy.zoom() * factor)),
      renderedPosition: { x: cy.width() / 2, y: cy.height() / 2 },
    });
  }, []);

  const fit = useCallback(() => {
    graphRef.current?.fit(undefined, 40);
  }, []);

  return { containerRef, zoom, fit };
}
