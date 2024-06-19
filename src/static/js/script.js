setTimeout(function() {
  const flashMessages = document.querySelectorAll('.flash-message');
  flashMessages.forEach(function(message) {
      message.style.transition = 'opacity 0.5s ease-out'; // Add transition effect
      message.style.opacity = '0'; // Fade out effect
      setTimeout(function() {
          message.remove(); // Remove from the DOM
      }, 500); // Wait for the fade-out transition to complete
  });
}, 5000); // 5000 milliseconds = 5 seconds
