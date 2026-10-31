import type { GraphNode, GraphResponse } from "../../models/Graph";
import { useCitationGraphViewModel } from "../../viewmodels/useCitationGraphViewModel";

interface CitationGraphProps {
  graph: GraphResponse;
  onSelectNode: (node: GraphNode | null) => void;
  onError: (message: string) => void;
}

export function CitationGraph({ graph, onSelectNode, onError }: CitationGraphProps) {
  const { containerRef, zoom, fit } = useCitationGraphViewModel(
    graph,
    onSelectNode,
    onError,
  );

  return (
    <div className="graph-card">
      <div className="graph-toolbar">
        <div className="graph-legend">
          <span><i className="legend-dot match-dot" /> Resultado da busca</span>
          <span><i className="legend-dot connected-dot" /> Artigo citado</span>
          <span><i className="legend-dot unavailable-dot" /> Sem metadados</span>
        </div>
        <div className="zoom-controls" aria-label="Controles de zoom do grafo">
          <button aria-label="Diminuir zoom" onClick={() => zoom(0.8)} type="button">−</button>
          <button aria-label="Aumentar zoom" onClick={() => zoom(1.25)} type="button">+</button>
          <button aria-label="Enquadrar grafo" onClick={fit} type="button">Enquadrar</button>
        </div>
      </div>
      <div
        aria-label="Grafo interativo de citações. Selecione um nó para ver os detalhes do artigo."
        className="graph-canvas"
        ref={containerRef}
        role="img"
      />
      <div className="graph-caption">
        <span><i className="arrow-key" aria-hidden="true">→</i> Sentido da citação</span>
        <span>Selecione um nó para ver o artigo</span>
      </div>
      {graph.truncated && (
        <div className="truncated-notice">
          O grafo exibe apenas as conexões mais relevantes. Refine a busca para ver
          resultados mais específicos.
        </div>
      )}
    </div>
  );
}
