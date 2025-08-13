document.getElementById("askBtn").addEventListener("click", async () => {
    const question = document.getElementById("question").value.trim();
    const answerDiv = document.getElementById("answer");

    if (!question) {
        answerDiv.innerHTML = "❌ لطفاً سوال خود را وارد کنید.";
        return;
    }

    answerDiv.innerHTML = "⏳ در حال دریافت پاسخ...";
    
    try {
        const res = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        const data = await res.json();
        answerDiv.innerHTML = data.answer;
    } catch (err) {
        answerDiv.innerHTML = "⚠ خطا در اتصال به سرور.";
    }
});
