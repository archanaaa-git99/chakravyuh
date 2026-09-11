import express from "express";
import cors from "cors";

const app = express();

app.use(cors());
app.use(express.json());

app.post("/investigate", (req, res) => {
  const wallet = req.body.wallet;

  console.log("Investigation request received:");
  console.log(wallet);

  res.json({
    wallet: wallet,
    risk: "HIGH",
    transactions: 24,
    blockchain_hops: 3,
    suspicious_points: 5,

    suspicious_activity: [
      {
        title: "Rapid fund movement",
        description:
          "Funds moved through multiple wallets within a short period.",
        severity: "HIGH"
      },
      {
        title: "Near-total forwarding",
        description:
          "96% of received funds were forwarded immediately.",
        severity: "HIGH"
      },
      {
        title: "Suspicious transition",
        description:
          "Wallet transition matches a known suspicious pattern.",
        severity: "MEDIUM"
      }
    ],

    vasp: {
      name: "Unknown Exchange",
      confidence: 78
    },

    connected_cases: [
      {
        id: "CH-1024",
        description: "Related wallet activity",
        type: "WALLET CONNECTION"
      },
      {
        id: "CH-1087",
        description: "Shared transaction pattern",
        type: "TRANSACTION PATTERN"
      }
    ]
  });
});

app.listen(5000, () => {
  console.log("================================");
  console.log("CHAKRAVYUH TEST BACKEND RUNNING");
  console.log("http://localhost:5000");
  console.log("================================");
});