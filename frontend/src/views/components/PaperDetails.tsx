import type { GraphNode } from "../../models/Graph";

const numberFormat = new Intl.NumberFormat("pt-BR");

interface PaperDetailsProps {
  node: GraphNode | null;
  onClose: () => void;
}

export function PaperDetails({ node, onClose }: PaperDetailsProps) {
  return (
    <aside className={`details-panel${node ? " has-selection" : ""}`}>
      <div className="details-heading">
        <span className="eyebrow">DETALHES DO ARTIGO</span>
        {node && (
          <button
            aria-label="Fechar detalhes do artigo"
            className="close-details"
            onClick={onClose}
            type="button"
          >×</button>
        )}
      </div>
      {node ? (
        <article className="paper-details">
          <span className={`paper-badge${node.is_match ? " is-match" : ""}`}>
            {node.is_match ? "RESULTADO DA BUSCA" : "CITAÇÃO"}
          </span>
          <h3>{node.title}</h3>
          <p className="paper-authors">
            {node.authors || "Informações sobre os autores indisponíveis"}
          </p>
          <div className="paper-id">
            <span>IDENTIFICADOR ARXIV</span>
            <strong>{node.paper_id ?? "Não disponível"}</strong>
          </div>
          {node.subjects && (
            <div className="paper-section">
              <h4>ASSUNTOS</h4>
              <p>{node.subjects}</p>
            </div>
          )}
          {node.abstract_excerpt && (
            <div className="paper-section">
              <h4>RESUMO</h4>
              <p>{node.abstract_excerpt}</p>
            </div>
          )}
          <div className="citation-stats">
            <div>
              <strong>{numberFormat.format(node.citations_received)}</strong>
              <span>Citações recebidas</span>
            </div>
            <div>
              <strong>{numberFormat.format(node.citations_made)}</strong>
              <span>Citações feitas</span>
            </div>
          </div>
          {node.is_match && (
            <div className="relevance-score">
              <span>RELEVÂNCIA NA BUSCA</span>
              <strong>{numberFormat.format(node.relevance_score)}</strong>
            </div>
          )}
        </article>
      ) : (
        <div className="details-placeholder">
          <span className="details-placeholder-icon" aria-hidden="true">
            <svg viewBox="0 0 32 32" fill="none">
              <path d="M9 5.5h9l5 5V26H9z" />
              <path d="M18 5.5v5h5M13 16h6M13 20h6" />
            </svg>
          </span>
          <strong>Conheça um artigo</strong>
          <p>Selecione um nó do grafo para ver detalhes, resumo e citações do artigo.</p>
        </div>
      )}
      <div className="details-footnote">
        A quantidade de citações mostra conexões, não a qualidade do artigo.
      </div>
    </aside>
  );
}
