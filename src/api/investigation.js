const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:5000";

export async function investigateWallet(walletAddress) {
  try {
    const response = await fetch(`${API_BASE_URL}/investigate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        wallet: walletAddress,
      }),
    });

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