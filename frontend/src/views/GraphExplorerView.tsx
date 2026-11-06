import type { GraphResponse, GraphNode } from "../models/Graph";
import type { useGraphExplorerViewModel } from "../viewmodels/useGraphExplorerViewModel";
import { CitationGraph } from "./components/CitationGraph";
import { PaperDetails } from "./components/PaperDetails";
import { SearchPanel } from "./components/SearchPanel";

const numberFormat = new Intl.NumberFormat("pt-BR");

type GraphExplorerViewModel = ReturnType<typeof useGraphExplorerViewModel>;

interface GraphExplorerViewProps {
  viewModel: GraphExplorerViewModel;
}

function ResultsPanel({
  graph,
  loading,
  error,
  onSelectNode,
  onError,
  onSearchSuggestion,
}: {
  graph: GraphResponse | null;
  loading: boolean;
  error: string | null;
  onSelectNode: (node: GraphNode | null) => void;
  onError: (message: string) => void;
  onSearchSuggestion: (query: string) => void;
}) {
  return (
    <section className="results-panel" aria-label="Resultados do grafo de citações">
      <div className="results-header">
        <div>
          <div className="eyebrow results-eyebrow">SEU ESPAÇO DE DESCOBERTAS</div>
          <h2>{graph ? `Resultados para “${graph.query}”` : "Rede de citações"}</h2>
        </div>
        {graph && (
          <div className="result-count">
            <strong>{numberFormat.format(graph.total_matches)}</strong>
            <span>{graph.total_matches === 1 ? "resultado" : "resultados"}</span>
          </div>
        )}
      </div>

      {error && (
        <div className="notice error-notice" role="alert">
          <span className="notice-symbol">!</span>
          <div><strong>Não foi possível concluir a busca</strong><p>{error}</p></div>
        </div>
      )}

      {!graph && !error && !loading && (
        <div className="empty-state">
          <div className="empty-illustration" aria-hidden="true">
            <span className="orbit orbit-one" />
            <span className="orbit orbit-two" />
            <span className="orbit-node node-a" />
            <span className="orbit-node node-b" />
            <span className="orbit-node node-c" />
            <span className="orbit-node node-center" />
          </div>
          <h3>As ideias estão todas conectadas.</h3>
          <p>Busque um tema ou artigo e descubra como as pesquisas se relacionam.</p>
          <div className="suggestions">
            <span>Experimente buscar</span>
            {["quantum field", "black holes", "string theory"].map((term) => (
              <button key={term} onClick={() => onSearchSuggestion(term)} type="button">
                {term}
              </button>
            ))}
          </div>
        </div>
      )}

      {loading && (
        <div className="loading-state" role="status">
          <span className="loading-orbit" />
          <strong>Mapeando conexões</strong>
          <span>Buscando artigos e suas relações de citação…</span>
        </div>
      )}

      {graph && !loading && graph.nodes.length === 0 && (
        <div className="empty-state no-results">
          <div className="no-results-mark" aria-hidden="true">?</div>
          <h3>Nenhum artigo encontrado</h3>
          <p>Tente uma palavra mais abrangente, outra grafia ou o nome de um autor.</p>
        </div>
      )}

      {graph && graph.nodes.length > 0 && !loading && (
        <CitationGraph graph={graph} onError={onError} onSelectNode={onSelectNode} />
      )}
    </section>
  );
}

export function GraphExplorerView({ viewModel }: GraphExplorerViewProps) {
  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Página inicial do ARCAG">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 32 32" fill="none">
              <path d="M7 23 14 9l5 8 4-5 5 11" />
              <circle cx="7" cy="23" r="2.5" />
              <circle cx="14" cy="9" r="2.5" />
              <circle cx="19" cy="17" r="2.5" />
              <circle cx="23" cy="12" r="2.5" />
              <circle cx="28" cy="23" r="2.5" />
            </svg>
          </span>
          <span className="brand-name">ARCAG</span>
          <span className="brand-divider" />
          <span className="brand-description">Explorador de grafos de citações</span>
        </a>
        <span className="topbar-caption">LITERATURA CIENTÍFICA CONECTADA</span>
      </header>

      <section className="workspace">
        <SearchPanel
          loading={viewModel.loading}
          onQueryChange={viewModel.setQuery}
          onSearch={viewModel.search}
          query={viewModel.query}
        />
        <ResultsPanel
          error={viewModel.error}
          graph={viewModel.graph}
          loading={viewModel.loading}
          onError={viewModel.reportError}
          onSearchSuggestion={viewModel.searchSuggestion}
          onSelectNode={viewModel.selectNode}
        />
        <PaperDetails
          node={viewModel.selectedNode}
          onClose={() => viewModel.selectNode(null)}
        />
      </section>

      <footer className="page-footer">
        <span>ARCAG <i>·</i> Explorando o conhecimento científico por meio de citações</span>
        <span>Baseado no conjunto de dados de pesquisa cit-HepTh</span>
      </footer>
    </main>
  );
}
