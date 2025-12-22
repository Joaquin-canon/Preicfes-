console.log("✅ JS Test Diagnóstico cargado (FINAL ESTABLE)");

document.addEventListener("DOMContentLoaded", function () {

  // =====================================================
  // ELEMENTOS
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

  if (!form || !tipoSelect || !contenedor || !bloqueDetalles) {
    console.error("❌ Elementos del modal faltantes");
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

  function abrir() {
    form.reset();
    tipoSelect.value = "";
    resetModal();
    modal.classList.remove("hidden");
  }

  function cerrar() {
    modal.classList.add("hidden");
    resetModal();
  }

  btnNueva?.addEventListener("click", abrir);
  btnCerrar?.addEventListener("click", cerrar);
  btnCancelar?.addEventListener("click", cerrar);
  backdrop?.addEventListener("click", cerrar);

  // =====================================================
  // RENDERS
  // =====================================================
  function renderOpciones() {
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

  function renderSMUR() {
    return renderOpciones();
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
          <option value="0">Solo I</option>
          <option value="1">Solo II</option>
          <option value="2">Ambas</option>
          <option value="3">Ninguna</option>
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
      ${renderOpciones()}
    `;
  }

  function renderImagen() {
    return `
      <div class="form-group">
        <label>Imagen</label>
        <input type="file" accept="image/*">
        <small>Por ahora solo referencia visual</small>
      </div>
      <div class="form-group">
        <label>Pregunta</label>
        <textarea id="pregunta_imagen" class="input-textarea"></textarea>
      </div>
      ${renderOpciones()}
    `;
  }

  // =====================================================
  // CAMBIO DE TIPO
  // =====================================================
  tipoSelect.addEventListener("change", () => {
    const tipo = tipoSelect.value;
    contenedor.innerHTML = "";

    if (!tipo) {
      resetModal();
      return;
    }

    bloqueDetalles.style.display = "block";

    if (tipo === "SMUR") contenedor.innerHTML = renderSMUR();
    else if (tipo === "AFIRMACIONES") contenedor.innerHTML = renderAfirmaciones();
    else if (tipo === "SMUR_CONTEXTO") contenedor.innerHTML = renderContexto();
    else if (tipo === "IMAGEN" || tipo === "TABLA") contenedor.innerHTML = renderImagen();
    else contenedor.innerHTML = "<p>Tipo no soportado</p>";
  });

  // =====================================================
  // SUBMIT
  // =====================================================
  form.addEventListener("submit", (e) => {
    const tipo = tipoSelect.value;

    // IMAGEN y TABLA = mismo flujo
    if (["SMUR","SMUR_CONTEXTO","IMAGEN","TABLA"].includes(tipo)) {
      const opciones = [...contenedor.querySelectorAll(".opcion")].map(o => o.value.trim());
      const resp = document.getElementById("respuesta_correcta_select");

      if (opciones.length !== 4 || opciones.some(o => !o)) {
        e.preventDefault();
        alert("Completa las 4 opciones");
        return;
      }

      document.getElementById("opciones_json").value = JSON.stringify(opciones);
      document.getElementById("respuesta_correcta").value = resp.value;
      return;
    }

    if (tipo === "AFIRMACIONES") {
      const afirmaciones = [...contenedor.querySelectorAll(".afirmacion")].map(a => a.value.trim());
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

    e.preventDefault();
    alert("Tipo no implementado");
  });

});
