// Função para retornar a URL base da API
function getApiBaseUrl() {
    return "http://127.0.0.1:8000/esportemuz/api/";
}

// Função para retornar o CSRF token do cookie
function getCsrfToken() {
    const name = "csrftoken=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookies = decodedCookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();

        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }

    return "";
}

// Função para inicializar o modal de formulário
function setupModalForm({ formId, modalId, endpoint, onSuccess }) {
    const form = document.getElementById(formId);
    const modalEl = document.getElementById(modalId);
    const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);

    modalEl.addEventListener('hidden.bs.modal', function () {
        document.activeElement.blur();
        form.reset();
        clearFormErrors(form);
    });

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        clearFormErrors(form);

        const formData = new FormData(form);
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: formData,
            });

            if (response.ok) {
                modal.hide();
                onSuccess();
            } else if (response.status === 400) {
                const data = await response.json();
                handleFormErrors(form, data);
            } else {
                console.error("Erro inesperado:", response.status);
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
        }
    });
}

// Função para lidar com erros de validação do formulário
function handleFormErrors(form, errors) {
    Object.entries(errors).forEach(([fieldName, messages]) => {
        const field = form.querySelector(`[name="${fieldName}"]`);

        if (field) {
            field.classList.add("is-invalid");

            const feedback = document.createElement("div");

            feedback.classList.add("invalid-feedback");

            feedback.innerText = messages.join(" ");

            field.after(feedback);
        }
    });
}

// Função para limpar erros de validação do formulário
function clearFormErrors(form) {
    form.querySelectorAll(".is-invalid").forEach(el => el.classList.remove("is-invalid"));
    form.querySelectorAll(".invalid-feedback").forEach(el => el.remove());
}

// Função para buscar dados de uma API
function fetchData(endpoint) {
    return fetch(endpoint)
        .then(response => {
            if (!response.ok) throw new Error('Erro ao buscar dados');
            return response.json();
        })
        .then(data => data.results || [])
        .catch(error => {
            console.error("Erro ao buscar dados:", error);
            return [];
        });
}

// Função para renderizar uma tabela
function renderTable({ endpoint, tableBodyId, columns }) {
    const tableBody = document.getElementById(tableBodyId);
    tableBody.innerHTML = '';

    fetchData(endpoint).then(data => {
        data.forEach(item => {
            const row = document.createElement("tr");

            columns.forEach(col => {
                const cell = document.createElement("td");

                if (typeof col === 'string') {
                    cell.textContent = item[col];
                } else if (typeof col === 'object') {
                    if (col.format) {
                        cell.textContent = col.format(item[col.key], item);
                    } else {
                        cell.textContent = item[col.key];
                    }
                }

                row.appendChild(cell);
            });

            tableBody.appendChild(row);
        });
    });
}

// Função para formatar a data
function formatDate(dateString) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    const date = new Date(dateString);

    return date.toLocaleDateString('pt-BR', options);
}