const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function investigateWallet(walletAddress) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/correlation/wallet/${encodeURIComponent(walletAddress)}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error("Investigation request failed.");
    }

    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Backend connection error:", error);
    throw error;
  }
}