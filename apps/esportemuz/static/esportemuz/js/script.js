// Função para confirmar exclusões
function confirmarExclusao(nome, tipo) {
	return confirm(`Tem certeza que deseja excluir ${tipo} "${nome}"? Esta ação não pode ser desfeita.`);
}

// Função para atualizar resultado de partida via AJAX
function atualizarResultado(partidaId, golsCasa, golsVisitante) {
	$.ajax({
		url: `/partidas/${partidaId}/resultado/`,
		type: 'POST',
		data: {
			'gols_casa': golsCasa,
			'gols_visitante': golsVisitante,
			'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()
		},
		success: function(response) {
			if (response.success) {
				location.reload();
			} else {
				alert('Erro: ' + response.message);
			}
		},
		error: function() {
			alert('Erro ao atualizar resultado.');
		}
	});
}