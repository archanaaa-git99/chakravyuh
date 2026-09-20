import { useState } from "react";
import TransactionGraph from "./TransactionGraph";
import { investigateWallet } from "./api/investigation";
import "./index.css";

function App() {
  const [walletAddress, setWalletAddress] = useState("");
  const [isInvestigating, setIsInvestigating] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [error, setError] = useState("");
  const [investigationData, setInvestigationData] = useState(null);

  const handleInvestigation = async () => {
    setError("");

    if (!walletAddress.trim()) {
      setError("Please enter a wallet address.");
      return;
    }

    setIsInvestigating(true);
    setShowDashboard(false);

    try {
      const data = await investigateWallet(walletAddress.trim());
      console.log("BACKEND RESPONSE:", data);

      setInvestigationData(data);
      setIsInvestigating(false);
      setShowDashboard(true);
    } catch (err) {
      console.error(err);
      setIsInvestigating(false);
      setError(
        "Could not connect to the investigation server. Make sure the backend is running."
      );
    }
  };

  if (isInvestigating) {
    return (
      <div className="loading-page">
        <div className="loading-container">
          <div className="loading-label">CHAKRAVYUH // DIGITAL FORENSICS</div>
          <h1>CHECKING WALLET</h1>
          <div className="loading-wallet">{walletAddress}</div>
          <div className="loading-warning">
            Checking this wallet against known cases. Please wait.
          </div>
        </div>
      </div>
    );
  }

  if (showDashboard) {
    const data = investigationData || {};

    return (
      <div className="dashboard-page">
        <header className="dashboard-header">
          <div>
            <div className="dashboard-brand">CHAKRAVYUH</div>
            <div className="dashboard-subtitle">
              BLOCKCHAIN INVESTIGATION SYSTEM
            </div>
          </div>
          <div className="investigation-status">● CHECK COMPLETE</div>
        </header>

        <section className="dashboard-intro">
          <div>
            <div className="eyebrow">INVESTIGATION TARGET</div>
            <h1>{data.wallet_address || walletAddress}</h1>
            <p>Correlation check completed successfully</p>
          </div>

          <div className="risk-badge">
            {data.has_overlap ? "CONNECTED" : "NO OVERLAP"}
          </div>
        </section>

        <section className="summary-grid">
          <div className="summary-card">
            <span>OVERLAP FOUND</span>
            <strong className="risk-text">
              {data.has_overlap ? "YES" : "NO"}
            </strong>
          </div>

          <div className="summary-card">
            <span>KNOWN ENTITY</span>
            <strong>{data.is_known_entity ? "YES" : "NO"}</strong>
          </div>

          <div className="summary-card">
            <span>ACTIVE CASE MATCHES</span>
            <strong>{data.overlapping_active_cases?.length || 0}</strong>
          </div>

          <div className="summary-card">
            <span>PAST CASE MATCHES</span>
            <strong>{data.overlapping_past_cases?.length || 0}</strong>
          </div>
        </section>

        <section className="dashboard-panel graph-panel">
          <div className="panel-heading">
            <div>
              <div className="eyebrow">CASE CORRELATION</div>
              <h2>Wallet Connection Graph</h2>
            </div>
          </div>

          <div className="graph-container">
            <TransactionGraph data={data} />
          </div>
        </section>

        {data.has_overlap && (
          <section className="dashboard-panel">
            <div className="eyebrow">CASE CORRELATION</div>
            <h2>Connected Cases</h2>

            <div className="case-list">
              {[
                ...(data.overlapping_active_cases || []).map((c) => ({
                  ...c,
                  type: "Active Case",
                })),
                ...(data.overlapping_past_cases || []).map((c) => ({
                  ...c,
                  type: "Past Case",
                })),
              ].map((item, index) => (
                <div className="case-item" key={index}>
                  <div>
                    <h3>CASE #{item.id ?? "unknown"}</h3>
                  </div>
                  <span>{item.type}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        <div className="report-section">
          <button
            className="report-button"
            onClick={() => {
              setShowDashboard(false);
              setWalletAddress("");
              setInvestigationData(null);
            }}
          >
            CHECK ANOTHER WALLET
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="landing-logo">CHAKRAVYUH</div>
        <div className="landing-system">BLOCKCHAIN INVESTIGATION SYSTEM</div>
      </header>

      <main className="hero-section">
        <div className="hero-eyebrow">DIGITAL FORENSICS PLATFORM</div>

        <h1>
          TRACE THE MONEY.
          <br />
          <span>UNCOVER THE TRUTH.</span>
        </h1>

        <p className="hero-description">
          Check a wallet address to see if it overlaps with other known
          fraud cases.
        </p>

        <div className="wallet-form">
          <input
            type="text"
            value={walletAddress}
            onChange={(e) => setWalletAddress(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleInvestigation();
              }
            }}
            placeholder="Enter wallet address..."
          />

          <button onClick={handleInvestigation}>INVESTIGATE →</button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {!error && (
          <div className="hero-hint">
            Enter a blockchain wallet address to begin investigation.
          </div>
        )}
      </main>
    </div>
  );
}

export default App;