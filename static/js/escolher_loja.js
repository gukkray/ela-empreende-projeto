// JavaScript
<script>
    $(document).ready(function(){
        $('#select-loja').change(function(){
            var lojaId = $(this).val();
            $.ajax({
                url: '/buscar-produtos-por-loja/',  // ajuste para a sua URL correta
                type: 'GET',
                data: {
                    loja_id: lojaId,
                },
                success: function(response){
                    var produtos = response.produtos;
                    var listaProdutos = $('#lista-produtos');
                    listaProdutos.empty();
                    produtos.forEach(function(produto){
                        listaProdutos.append('<p>' + produto.nome + '</p>');
                    });
                },
                error: function(error){
                    console.log(error);
                }
            });
        })
    });
</script>
