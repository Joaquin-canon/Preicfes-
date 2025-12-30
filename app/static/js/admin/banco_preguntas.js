console.log("✅ JS Banco de Preguntas cargado (FINAL DEFINITIVO)");

document.addEventListener("DOMContentLoaded", () => {

  // =============================
  // ELEMENTOS
  // =============================
  const btnNueva = document.getElementById("btn-nueva-pregunta");
  const modal = document.getElementById("modal-nueva-pregunta");
  const btnCerrar = document.getElementById("btn-cerrar-modal");
  const btnCancelar = document.getElementById("btn-cancelar");
  const backdrop = document.getElementById("modal-backdrop");

  const form = document.getElementById("form-nueva-pregunta");
  const tipoSelect = document.getElementById("tipo_pregunta");
  const contenedor = document.getElementById("contenedor-formulario-dinamico");
  const bloqueDetalles = document.getElementById("bloque-detalles");
  const bloqueImagen = document.getElementById("bloque-imagen");
  const bloqueContexto = document.getElementById("bloque-contexto");

  if (!form || !tipoSelect || !contenedor || !bloqueDetalles) {
    console.error("❌ Elementos del modal faltantes");
    return;
  }

  // =============================
  // MODAL
  // =============================
  function resetModal() {
    bloqueDetalles.style.display = "none";
    if (bloqueImagen) bloqueImagen.style.display = "none";
    if (bloqueContexto) bloqueContexto.style.display = "none";
    contenedor.innerHTML = "";
    document.getElementById("opciones_json").value = "";
    document.getElementById("respuesta_correcta").value = "";
  }

  function abrirModal() {
    resetModal();
    modal.classList.remove("hidden");
  }

  function cerrarModal() {
    modal.classList.add("hidden");
    resetModal();
  }

  btnNueva?.addEventListener("click", abrirModal);
  btnCerrar?.addEventListener("click", cerrarModal);
  btnCancelar?.addEventListener("click", cerrarModal);
  backdrop?.addEventListener("click", cerrarModal);

  // =============================
  // RENDERS
  // =============================
  const renderOpciones = () => `
    <div class="space-y-2">
      <label class="text-sm font-medium">Opciones</label>
      <input class="opcion border rounded p-2 w-full" placeholder="Opción A">
      <input class="opcion border rounded p-2 w-full" placeholder="Opción B">
      <input class="opcion border rounded p-2 w-full" placeholder="Opción C">
      <input class="opcion border rounded p-2 w-full" placeholder="Opción D">
    </div>
    <div>
      <label class="text-sm font-medium">Respuesta correcta</label>
      <select id="respuesta_correcta_select" class="border rounded p-2 w-full">
        <option value="0">A</option>
        <option value="1">B</option>
        <option value="2">C</option>
        <option value="3">D</option>
      </select>
    </div>
  `;

  const renderAfirmaciones = () => `
    <div>
      <label>Afirmación I</label>
      <textarea class="afirmacion border rounded p-2 w-full"></textarea>
    </div>
    <div>
      <label>Afirmación II</label>
      <textarea class="afirmacion border rounded p-2 w-full"></textarea>
    </div>
    <div>
      <label>Respuesta correcta</label>
      <select id="respuesta_correcta_select" class="border rounded p-2 w-full">
        <option value="0">Solo I</option>
        <option value="1">Solo II</option>
        <option value="2">Ambas</option>
        <option value="3">Ninguna</option>
      </select>
    </div>
  `;

  // =============================
  // CAMBIO DE TIPO
  // =============================
  tipoSelect.addEventListener("change", () => {
    const option = tipoSelect.selectedOptions[0];

    contenedor.innerHTML = "";
    if (bloqueImagen) bloqueImagen.style.display = "none";
    if (bloqueContexto) bloqueContexto.style.display = "none";

    if (!option || !option.value) {
      bloqueDetalles.style.display = "none";
      return;
    }

    bloqueDetalles.style.display = "block";

    const usaImagen =
      option.dataset.usaImagen === "true" ||
      option.dataset.usaImagen === "True" ||
      option.dataset.usaImagen === "1";

    const usaContexto =
      option.dataset.usaContexto === "true" ||
      option.dataset.usaContexto === "True" ||
      option.dataset.usaContexto === "1";

    if (usaContexto && bloqueContexto) {
      bloqueContexto.style.display = "block";
    }

    if (usaImagen && bloqueImagen) {
      bloqueImagen.style.display = "block";
    }

    // 🔥 decisión del formulario
    if (option.textContent.toLowerCase().includes("afirm")) {
      contenedor.innerHTML = renderAfirmaciones();
    } else {
      contenedor.innerHTML = renderOpciones();
    }
  });

  // =============================
  // SUBMIT
  // =============================
  form.addEventListener("submit", (e) => {

    const option = tipoSelect.selectedOptions[0];
    if (!option) return;

    const usaImagen =
      option.dataset.usaImagen === "true" ||
      option.dataset.usaImagen === "True" ||
      option.dataset.usaImagen === "1";

    const esAfirmaciones =
      option.textContent.toLowerCase().includes("afirm");

    if (esAfirmaciones) {
      const afirmaciones = [...contenedor.querySelectorAll(".afirmacion")]
        .map(a => a.value.trim());

      const resp = document.getElementById("respuesta_correcta_select");

      if (afirmaciones.length !== 2 || afirmaciones.some(a => !a)) {
        e.preventDefault();
        alert("Completa ambas afirmaciones");
        return;
      }

      document.getElementById("opciones_json").value = JSON.stringify(afirmaciones);
      document.getElementById("respuesta_correcta").value = resp.value;
      return;
    }

    // Opciones
    const opciones = [...contenedor.querySelectorAll(".opcion")]
      .map(o => o.value.trim());

    const resp = document.getElementById("respuesta_correcta_select");

    if (opciones.length !== 4 || opciones.some(o => !o)) {
      e.preventDefault();
      alert("Completa las 4 opciones");
      return;
    }

    if (usaImagen) {
      const inputImagen = form.querySelector('input[name="imagen"]');
      if (!inputImagen || inputImagen.files.length === 0) {
        e.preventDefault();
        alert("Debes seleccionar una imagen");
        return;
      }
    }

    document.getElementById("opciones_json").value = JSON.stringify(opciones);
    document.getElementById("respuesta_correcta").value = resp.value;
  });

});
