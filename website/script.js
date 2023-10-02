document.addEventListener("DOMContentLoaded", function () {
    const chatbotIcon = document.getElementById("chatbot-icon");
    const chatbotIframe = document.getElementById("chatbot-iframe");

    let isOpen = false;

    chatbotIcon.addEventListener("click", function () {
        isOpen = !isOpen;
        chatbotIframe.style.display = isOpen ? "block" : "none";
    });
});
