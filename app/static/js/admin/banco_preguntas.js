console.log("✅ JS Banco de Preguntas cargado (ESTABLE FINAL)");

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

  if (!form || !tipoSelect || !contenedor || !bloqueDetalles) {
    console.error("❌ Elementos del modal faltantes");
    return;
  }

  // =============================
  // MODAL
  // =============================
  function resetModal() {
    bloqueDetalles.classList.add("hidden");
    contenedor.innerHTML = "";
    document.getElementById("opciones_json").value = "";
    document.getElementById("respuesta_correcta").value = "";
  }

  function abrirModal() {
    form.reset();
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
    <div class="space-y-2">
      <label>Afirmación I</label>
      <textarea class="afirmacion border rounded p-2 w-full"></textarea>
    </div>
    <div class="space-y-2">
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

  const renderContexto = () => `
    <div>
      <label>Texto / Contexto</label>
      <textarea class="border rounded p-2 w-full mb-2"></textarea>
    </div>
    <div>
      <label>Pregunta</label>
      <textarea class="border rounded p-2 w-full mb-2"></textarea>
    </div>
    ${renderOpciones()}
  `;

  const renderImagen = () => `
    <div>
      <label>Imagen</label>
      <input type="file" accept="image/*" class="border rounded p-2 w-full mb-2">
    </div>
    <div>
      <label>Pregunta</label>
      <textarea class="border rounded p-2 w-full mb-2"></textarea>
    </div>
    ${renderOpciones()}
  `;

  // =============================
  // CAMBIO DE TIPO
  // =============================
  tipoSelect.addEventListener("change", () => {
    const tipo = tipoSelect.value;
    contenedor.innerHTML = "";

    if (!tipo) {
      bloqueDetalles.classList.add("hidden");
      return;
    }

    bloqueDetalles.classList.remove("hidden");

    if (tipo === "SMUR") {
      contenedor.innerHTML = renderOpciones();
    }
    else if (tipo === "AFIRMACIONES") {
      contenedor.innerHTML = renderAfirmaciones();
    }
    else if (tipo === "SMUR_CONTEXTO") {
      contenedor.innerHTML = renderContexto();
    }
    else if (tipo === "IMAGEN") {
      contenedor.innerHTML = renderImagen();
    }
    else if (tipo === "TABLA") {
      contenedor.innerHTML = renderImagen(); // reutiliza
    }
    else {
      contenedor.innerHTML = `
        <p class="text-sm text-red-500">
          Tipo no soportado: ${tipo}
        </p>
      `;
    }
  });

  // =============================
  // SUBMIT
  // =============================
  form.addEventListener("submit", (e) => {
    const tipo = tipoSelect.value;

    if (["SMUR", "SMUR_CONTEXTO", "IMAGEN", "TABLA"].includes(tipo)) {
      const opciones = [...contenedor.querySelectorAll(".opcion")]
        .map(o => o.value.trim());

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

    e.preventDefault();
    alert("Tipo no implementado");
  });

});

document.querySelectorAll('.btn-editar').forEach(btn => {
    btn.addEventListener('click', () => {
        abrirModal();

        document.querySelector('[name="area_id"]').value = btn.dataset.area;
        document.querySelector('[name="tipo_pregunta_codigo"]').value = btn.dataset.tipo;
        document.querySelector('[name="dificultad"]').value = btn.dataset.dificultad;
        document.querySelector('[name="enunciado"]').value = btn.dataset.enunciado;

        const opciones = JSON.parse(btn.dataset.opciones);
        renderOpciones(opciones, btn.dataset.correcta);

        document.getElementById('form-nueva-pregunta').action =
            `/admin/catalogo/preguntas/${btn.dataset.id}/editar`;
    });
});
