/* ============================================================
   APP.JS - JavaScript principal de SportField
   Este archivo agrega interactividad a la aplicación.
   Se carga al final del body en base.html.
   ============================================================ */

// -------------------------------------------------------
// Auto-ocultar mensajes flash después de 5 segundos
// -------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {

  // Seleccionamos todos los mensajes flash
  const messages = document.querySelectorAll('.message');

  messages.forEach(function (msg) {
    // Después de 5 segundos, ocultamos el mensaje con animación
    setTimeout(function () {
      msg.style.transition = 'all 0.4s ease';
      msg.style.opacity = '0';
      msg.style.transform = 'translateX(120%)';
      // Después de la animación, lo removemos del DOM
      setTimeout(function () { msg.remove(); }, 400);
    }, 5000);
  });

  // -------------------------------------------------------
  // Confirmar antes de eliminar (botones de eliminar)
  // Busca todos los enlaces que van a URLs de "eliminar"
  // -------------------------------------------------------
  document.querySelectorAll('a[href*="eliminar"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      // Si el usuario presiona Cancelar, no navega
      if (!confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
        e.preventDefault();
      }
    });
  });

  // -------------------------------------------------------
  // Resaltar fila de tabla al hacer clic
  // -------------------------------------------------------
  document.querySelectorAll('.data-table tbody tr').forEach(function (row) {
    row.addEventListener('click', function () {
      // Primero quitamos el resaltado de otras filas
      document.querySelectorAll('.data-table tbody tr').forEach(r => r.classList.remove('row-selected'));
      // Luego resaltamos la fila clickeada
      this.classList.add('row-selected');
    });
  });

  // -------------------------------------------------------
  // Animación de entrada para las tarjetas (item-card)
  // Usa IntersectionObserver para animar cuando son visibles
  // -------------------------------------------------------
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target); // Solo anima una vez
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.item-card, .stat-card').forEach(function (card, i) {
    // Estado inicial: invisible y desplazada hacia abajo
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = `opacity 0.4s ease ${i * 0.05}s, transform 0.4s ease ${i * 0.05}s`;
    observer.observe(card);
  });

});
