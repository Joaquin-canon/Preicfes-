console.log("✅ JS Test Diagnóstico cargado (UNIFICADO Y COMPLETO)");

document.addEventListener("DOMContentLoaded", function () {

  // =====================================================
  // ELEMENTOS PRINCIPALES
  // =====================================================
  const btnNueva = document.getElementById("btn-nueva-pregunta");
  const modal = document.getElementById("modal-nueva-pregunta");
  const btnCerrar = document.getElementById("btn-cerrar-modal");
  const btnCancelar = document.getElementById("btn-cancelar");
  const backdrop = document.getElementById("modal-backdrop");

  const form = document.getElementById("form-nueva-pregunta");
  const tipoSelect = document.getElementById("tipo_pregunta");
  const contenedor = document.getElementById("contenedor-formulario-dinamico");
  const bloqueDetalles = document.getElementById("bloque-detalles");

  if (!btnNueva || !modal || !form || !tipoSelect || !contenedor || !bloqueDetalles) {
    console.error("❌ Elementos del modal incompletos");
    return;
  }

  // =====================================================
  // HELPERS
  // =====================================================
  function resetModal() {
    bloqueDetalles.style.display = "none";
    contenedor.innerHTML = "";
    document.getElementById("opciones_json").value = "";
    document.getElementById("respuesta_correcta").value = "";
  }

  function abrirModal() {
    form.reset();
    tipoSelect.value = "";
    resetModal();
    modal.classList.remove("hidden");
    modal.setAttribute("aria-hidden", "false");
  }

  function cerrarModal() {
    modal.classList.add("hidden");
    modal.setAttribute("aria-hidden", "true");
    resetModal();
  }

  btnNueva.addEventListener("click", abrirModal);
  btnCerrar.addEventListener("click", cerrarModal);
  btnCancelar.addEventListener("click", cerrarModal);
  backdrop.addEventListener("click", cerrarModal);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.classList.contains("hidden")) {
      cerrarModal();
    }
  });

  // =====================================================
  // FORMULARIOS POR TIPO
  // =====================================================
  function renderSMUR() {
    return `
      <div class="form-group">
        <label>Opciones</label>
        <input class="input-text opcion" placeholder="Opción A">
        <input class="input-text opcion" placeholder="Opción B">
        <input class="input-text opcion" placeholder="Opción C">
        <input class="input-text opcion" placeholder="Opción D">
      </div>
      <div class="form-group">
        <label>Respuesta correcta</label>
        <select id="respuesta_correcta_select" class="input-select">
          <option value="0">A</option>
          <option value="1">B</option>
          <option value="2">C</option>
          <option value="3">D</option>
        </select>
      </div>
    `;
  }

  function renderAfirmaciones() {
    return `
      <div class="form-group">
        <label>Afirmación I</label>
        <textarea class="input-textarea afirmacion"></textarea>
      </div>
      <div class="form-group">
        <label>Afirmación II</label>
        <textarea class="input-textarea afirmacion"></textarea>
      </div>
      <div class="form-group">
        <label>Respuesta correcta</label>
        <select id="respuesta_correcta_select" class="input-select">
          <option value="0">Solo I es correcta</option>
          <option value="1">Solo II es correcta</option>
          <option value="2">Ambas son correctas</option>
          <option value="3">Ninguna es correcta</option>
        </select>
      </div>
    `;
  }

  function renderContexto() {
    return `
      <div class="form-group">
        <label>Texto / Contexto</label>
        <textarea id="texto_contexto" class="input-textarea"></textarea>
      </div>
      <div class="form-group">
        <label>Pregunta</label>
        <textarea id="pregunta_contexto" class="input-textarea"></textarea>
      </div>
      ${renderSMUR()}
    `;
  }

  function renderImagen() {
    return `
      <div class="form-group">
        <label>Descripción de la imagen</label>
        <textarea id="descripcion_imagen" class="input-textarea"></textarea>
      </div>
      <div class="form-group">
        <label>URL de la imagen</label>
        <input id="url_imagen" class="input-text" placeholder="https://...">
      </div>
      ${renderSMUR()}
    `;
  }

  function renderTabla() {
    return `
      <div class="form-group">
        <label>Datos de la tabla</label>
        <textarea id="datos_tabla" class="input-textarea"
          placeholder="Ej: filas y columnas en texto"></textarea>
      </div>
      ${renderSMUR()}
    `;
  }

  // =====================================================
  // CAMBIO DE TIPO
  // =====================================================
  tipoSelect.addEventListener("change", () => {
    const tipo = (tipoSelect.value || "").trim();
    contenedor.innerHTML = "";

    if (!tipo) {
      resetModal();
      return;
    }

    bloqueDetalles.style.display = "block";

    if (tipo === "SMUR") contenedor.innerHTML = renderSMUR();
    else if (tipo === "AFIRMACIONES") contenedor.innerHTML = renderAfirmaciones();
    else if (tipo === "SMUR_CONTEXTO") contenedor.innerHTML = renderContexto();
    else if (tipo === "IMAGEN") contenedor.innerHTML = renderImagen();
    else if (tipo === "TABLA") contenedor.innerHTML = renderTabla();
    else contenedor.innerHTML = `<p>Tipo no soportado.</p>`;
  });

  // =====================================================
  // SUBMIT
  // =====================================================
  form.addEventListener("submit", (e) => {
    const tipo = (tipoSelect.value || "").trim();

    const opciones = [...contenedor.querySelectorAll(".opcion")].map(o => o.value.trim());
    const resp = document.getElementById("respuesta_correcta_select");

    if (["SMUR","SMUR_CONTEXTO","IMAGEN","TABLA"].includes(tipo)) {
      if (opciones.length !== 4 || opciones.some(o => !o)) {
        e.preventDefault();
        alert("Completa las 4 opciones.");
        return;
      }
      document.getElementById("opciones_json").value = JSON.stringify(opciones);
      document.getElementById("respuesta_correcta").value = resp.value;
      return;
    }

    if (tipo === "AFIRMACIONES") {
      const afirmaciones = [...contenedor.querySelectorAll(".afirmacion")].map(a => a.value.trim());
      if (afirmaciones.length !== 2 || afirmaciones.some(a => !a)) {
        e.preventDefault();
        alert("Completa ambas afirmaciones.");
        return;
      }
      document.getElementById("opciones_json").value = JSON.stringify(afirmaciones);
      document.getElementById("respuesta_correcta").value = resp.value;
      return;
    }

    e.preventDefault();
    alert("Tipo de pregunta no válido.");
  });

});
