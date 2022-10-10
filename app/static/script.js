function redirecionar() {
    usuario = document.getElementById('pesquisar').value
    document.location.href = `user/${usuario}`
}

const titulo = document.getElementById('titulo')
titulo.addEventListener('click', function(){
    document.location.href = '/'
})
