// safetap.js - Handles transaction form and backend connection with enhanced UI feedback

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("transactionForm");
  const resultBox = document.getElementById("resultBox");
  const riskScoreEl = document.getElementById("risk_score");
  const stepUpEl = document.getElementById("step_up");
  const submitBtn = form.querySelector("button[type='submit']");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Disable button and show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Evaluating...';

    const user_id = document.getElementById("user_id").value;
    const device_id = document.getElementById("device_id").value;
    const amount = parseFloat(document.getElementById("amount").value);
    const time_of_day = document.getElementById("time_of_day").value;

    const data = { user_id, device_id, amount, time_of_day };

    try {
      const response = await fetch("http://127.0.0.1:8000/transaction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error("Failed to get response from backend.");
      }

      const result = await response.json();

      riskScoreEl.textContent = result.risk_score;
      stepUpEl.textContent = result.step_up_required ? "Yes" : "No";

      // Set alert class based on risk level
      resultBox.className = "alert mt-4";
      resultBox.classList.remove("d-none");
      if (result.risk_score === "HIGH") {
        resultBox.classList.add("alert-danger");
      } else if (result.risk_score === "MEDIUM") {
        resultBox.classList.add("alert-warning");
      } else {
        resultBox.classList.add("alert-success");
      }

    } catch (err) {
      alert("Error: " + err.message);
      console.error(err);
    } finally {
      // Restore button
      submitBtn.disabled = false;
      submitBtn.textContent = "Evaluate Risk";
    }
  });
});
