// frontend/script.js

document.addEventListener("DOMContentLoaded", () => {
    const btnAtualizar = document.getElementById("btnAtualizar");
    const btnNovo = document.getElementById("btnNovoPaciente");
    const modal = document.getElementById("modalPaciente");
    const fecharModal = document.getElementById("fecharModal");
    const cancelar = document.getElementById("cancelar");
    const form = document.getElementById("formPaciente");
    const tabela = document.getElementById("tabela-fila");
    const alerta = document.getElementById("alerta");
  
    const carregarFila = async () => {
      alerta.classList.add("hidden");
      tabela.innerHTML = "<tr><td colspan='6' class='text-center py-4 text-gray-400'>Carregando...</td></tr>";
  
      try {
        const res = await fetch("http://localhost:8000/api/v1/fila");
        const json = await res.json();
  
        if (!json.success) throw new Error(json.message || "Erro ao carregar fila");
  
        if (!json.data.length) {
          tabela.innerHTML = "<tr><td colspan='6' class='text-center py-4'>Nenhum paciente na fila.</td></tr>";
          return;
        }
  
        tabela.innerHTML = "";
        json.data.forEach((item, i) => {
          const tr = document.createElement("tr");
          tr.className = "hover:bg-gray-50 transition";
          tr.innerHTML = `
            <td class="px-4 py-2 font-semibold">${i + 1}</td>
            <td class="px-4 py-2">${item.nome}</td>
            <td class="px-4 py-2">${item.escore}</td>
            <td class="px-4 py-2 capitalize">${item.prioridade}</td>
            <td class="px-4 py-2">${item.idade}</td>
            <td class="px-4 py-2">${new Date(item.data_primeira_consulta).toLocaleDateString()}</td>
          `;
          tabela.appendChild(tr);
        });
      } catch (err) {
        alerta.textContent = err.message;
        alerta.classList.remove("hidden");
        tabela.innerHTML = "<tr><td colspan='6' class='text-center py-4 text-red-400'>Erro ao carregar.</td></tr>";
      }
    };
  
    // Abrir e fechar modal
    btnNovo.onclick = () => modal.classList.remove("hidden");
    fecharModal.onclick = () => modal.classList.add("hidden");
    cancelar.onclick = () => modal.classList.add("hidden");
  
    // Enviar novo paciente
    form.onsubmit = async (e) => {
      e.preventDefault();
      const dados = Object.fromEntries(new FormData(form));
      try {
        const res = await fetch("http://localhost:8000/api/v1/pacientes", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(dados),
        });
        const json = await res.json();
        if (!json.success) throw new Error(json.message || "Erro ao criar paciente");
  
        alerta.textContent = "Paciente criado com sucesso!";
        alerta.classList.remove("hidden");
        alerta.classList.replace("bg-yellow-100", "bg-green-100");
        modal.classList.add("hidden");
        form.reset();
        carregarFila();
      } catch (err) {
        alerta.textContent = err.message;
        alerta.classList.remove("hidden");
        alerta.classList.replace("bg-yellow-100", "bg-red-100");
      }
    };
  
    btnAtualizar.onclick = carregarFila;
    carregarFila();
  });
  