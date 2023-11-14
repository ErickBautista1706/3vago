$(document).ready(function() {
    console.log("Hora de chambear :p");

    $(".home").click(function(){
        mostrarDash();
    });

    $(".users").click(function(){
        mostrarUsers();
    });

    $(".actionEdit").click(function() {
        var id = $(this).data("id");
        $("#usuario_id").val(id);
        console.log("Obtuve el id:", id);
    });

    $(".actionDelete").click(function() {
        var id = $(this).data("id");
        console.log("Obtuve el id:", id);
        Swal.fire({
            title: '¿Estás seguro?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                eliminarUsuario(id);
            }
        });
    });
    
   
    
      
    
    




});


function mostrarDash(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    divInico.style.display = 'block';
    divUsers.style.display = 'none';

}

function mostrarUsers(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    divInico.style.display = 'none';
    divUsers.style.display = 'block';
}


function eliminarUsuario(id) {
    $.ajax({
        url: "/eliminar_usuario/" + id,
        type: "GET",
        success: function(response) {
            if (response.success) {
                
                console.log("Usuario eliminado exitosamente.");
            } else {
                console.error("Error al eliminar usuario.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}


