
function metodo(){
    let modalregistros = document.getElementById("modal-registros")
    let ocultar = document.getElementById("ocultar")
    let qrimage = document.getElementById("contqrimage")
    qrimage.style.display = "none"
    modalregistros.style.display = "block"
}

function viewimage(event) {
    var reader = new FileReader();
    reader.onload = function(){
        var output = document.getElementById('imagePreview');
        output.innerHTML = '<img src="'+reader.result+'" alt="Vista previa de la imagen" class="rounded mx-auto d-block col-5 mb-3" style="width: 200px; height: 200px;">';
    };
    reader.readAsDataURL(event.target.files[0]);
}


let botonesEliminar = document.querySelectorAll(".eliminar");
botonesEliminar.forEach((boton) =>{
    boton.addEventListener("click",function(e){
        let posicion = e.target.dataset.id
        console.log(posicion)
    })

})
