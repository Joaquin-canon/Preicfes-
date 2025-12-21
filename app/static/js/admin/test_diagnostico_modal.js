console.log("✅ JS NUEVO CARGADO - v5");

document.addEventListener("DOMContentLoaded", function () {

  const btnNueva = document.getElementById("btn-nueva-pregunta");
  const modal = document.getElementById("modal-nueva-pregunta");
  const btnCerrar = document.getElementById("btn-cerrar-modal");
  const btnCancelar = document.getElementById("btn-cancelar");
  const backdrop = document.getElementById("modal-backdrop");

  const form = document.getElementById("form-nueva-pregunta");
  const tipoSelect = document.getElementById("tipo_pregunta");
  const contenedor = document.getElementById("contenedor-formulario-dinamico");
  const bloqueDetalles = document.getElementById("bloque-detalles");

  // Validación de existencia
  const faltantes = [];
  if (!btnNueva) faltantes.push("btn-nueva-pregunta");
  if (!modal) faltantes.push("modal-nueva-pregunta");
  if (!btnCerrar) faltantes.push("btn-cerrar-modal");
  if (!btnCancelar) faltantes.push("btn-cancelar");
  if (!form) faltantes.push("form-nueva-pregunta");
  if (!tipoSelect) faltantes.push("tipo_pregunta");
  if (!contenedor) faltantes.push("contenedor-formulario-dinamico");
  if (!bloqueDetalles) faltantes.push("bloque-detalles");

  if (faltantes.length) {
    console.error("❌ Faltan elementos del modal:", faltantes);
    return;
  }

  // --------------------
  // Helpers
  // --------------------
  function resetModal() {
    // ✅ oculta todo lo demás (clave para tu requerimiento)
    bloqueDetalles.style.display = "none";
    contenedor.innerHTML = "";

    // limpia hidden fields
    const hOpc = document.getElementById("opciones_json");
    const hResp = document.getElementById("respuesta_correcta");
    if (hOpc) hOpc.value = "";
    if (hResp) hResp.value = "";
  }

  // --------------------
  // Abrir / cerrar modal
  // --------------------
  function abrir(e) {
    if (e) e.preventDefault();

    form.reset();
    tipoSelect.value = "";
    resetModal(); // ✅ deja solo tipo visible

    modal.classList.remove("hidden");
    modal.setAttribute("aria-hidden", "false");
  }

  function cerrar() {
    modal.classList.add("hidden");
    modal.setAttribute("aria-hidden", "true");

    form.reset();
    tipoSelect.value = "";
    resetModal();
  }

  btnNueva.addEventListener("click", abrir);
  btnCerrar.addEventListener("click", cerrar);
  btnCancelar.addEventListener("click", cerrar);
  backdrop.addEventListener("click", cerrar);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !modal.classList.contains("hidden")) cerrar();
  });

  // --------------------
  // Formulario dinámico
  // --------------------
  function renderSMUR() {
    return `
      <div class="form-group">
        <label>Opciones (SMUR)</label>
        <input class="input-text" id="opA" placeholder="Opción A" required>
        <input class="input-text" id="opB" placeholder="Opción B" required>
        <input class="input-text" id="opC" placeholder="Opción C" required>
        <input class="input-text" id="opD" placeholder="Opción D" required>
      </div>

      <div class="form-group">
        <label>Respuesta correcta</label>
        <select class="input-select" id="respuesta_correcta_select" required>
          <option value="0">A</option>
          <option value="1">B</option>
          <option value="2">C</option>
          <option value="3">D</option>
        </select>
      </div>
    `;
  }

  // ✅ Mostrar el resto SOLO cuando se seleccione tipo
  tipoSelect.addEventListener("change", () => {
    contenedor.innerHTML = "";
    const codigo = (tipoSelect.value || "").trim();

    if (!codigo) {
      resetModal();
      return;
    }

    // ✅ ahora sí mostramos área/dificultad/enunciado
    bloqueDetalles.style.display = "block";

    if (codigo === "SMUR") {
      contenedor.innerHTML = renderSMUR();
      return;
    }

    contenedor.innerHTML = `
      <div class="form-group">
        <p style="margin:0;">Formulario para <b>${codigo}</b> aún no implementado.</p>
      </div>
    `;
  });

  // --------------------
  // Submit: llenar hidden
  // --------------------
  form.addEventListener("submit", (e) => {
    const tipo = (tipoSelect.value || "").trim();

    if (tipo !== "SMUR") {
      e.preventDefault();
      alert("Ese tipo de pregunta aún no está implementado.");
      return;
    }

    const opA = document.getElementById("opA");
    const opB = document.getElementById("opB");
    const opC = document.getElementById("opC");
    const opD = document.getElementById("opD");
    const sel = document.getElementById("respuesta_correcta_select");

    if (!opA || !opB || !opC || !opD || !sel) {
      e.preventDefault();
      alert("Primero selecciona el tipo SMUR y completa las opciones.");
      return;
    }

    const opciones = [
      opA.value.trim(),
      opB.value.trim(),
      opC.value.trim(),
      opD.value.trim(),
    ];

    if (opciones.some(o => !o)) {
      e.preventDefault();
      alert("Completa todas las opciones A, B, C y D.");
      return;
    }

    const correcta = parseInt(sel.value, 10);

    document.getElementById("opciones_json").value = JSON.stringify(opciones);
    document.getElementById("respuesta_correcta").value = String(correcta);
  });

});
