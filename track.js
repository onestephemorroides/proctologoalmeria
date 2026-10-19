/* Medición de contactos: clics en teléfono y WhatsApp (Google Analytics 4) */
(function () {
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || typeof gtag !== 'function') return;
    var h = a.getAttribute('href') || '';
    var name = null;
    if (h.indexOf('tel:') === 0) name = 'phone_click';
    else if (h.indexOf('wa.me/') > -1 || h.indexOf('api.whatsapp.com') > -1) name = 'whatsapp_click';
    if (!name) return;
    gtag('event', name, {
      link_url: h.split('?')[0],
      page_path: location.pathname,
      transport_type: 'beacon'
    });
  }, true);
})();
