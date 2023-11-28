
$(document).ready(function() {
    
    console.log("Hora de chambear :p");

    $(".home").click(function(){
        mostrarDash();
    });

    $(".users").click(function(){
        mostrarUsers();
    });

    $(".zone").click(function(){
        mostrarZona();
    });


    $(".actionEdit").click(function() {
        var id = $(this).data("id");
        get_data_user(id)
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
    
    $(".del-zone").click(function(){
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
                eliminar_zona(id);
            }
        });
    });

    


    $(".edit-zone").click(function() {
        var id = $(this).data("id");
        get_data_zona(id);
    });
   
    
      
    
    




});


function mostrarDash(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    var divZonas = document.getElementById("divZona");
    divInico.style.display = 'block';
    divUsers.style.display = 'none';
    divZonas.style.display = 'none';

}

function mostrarUsers(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    var divZonas = document.getElementById("divZona");
    divInico.style.display = 'none';
    divUsers.style.display = 'block';
    divZonas.style.display = 'none';
}

function mostrarZona(){
    var divInico = document.getElementById("divInicio");
    var divUsers = document.getElementById("divUsuarios");
    var divZonas = document.getElementById("divZona");
    divInico.style.display = 'none';
    divUsers.style.display = 'none';
    divZonas.style.display = 'block';

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

function get_data_user(id){
    $.ajax({
        url: "/get_usuario_info/" + id,
        type: "GET",
        success: function(response) {
            console.log("Respuesta completa del servidor:", response);

            if (response.success) {
                var datos_usuario = response.usuario;
                $("#id_usr").val(response.usuario.id_usr);
                $("#id_usr_act").val(datos_usuario[0]);
                $("#nombre_act").val(datos_usuario[1]);
                $("#apellidoP_act").val(datos_usuario[2]);
                $("#apellidoM_act").val(datos_usuario[3]);
                $("#alias_act").val(datos_usuario[4]);
                $("#email_act").val(datos_usuario[5]);
                $("#psw_act").val(datos_usuario[6]);
                $("#tipoUsuario_act").val(datos_usuario[7]);

                // Mostrar el modal de actualización
                $("#modalActualizarUsuario").modal("show");

            } else {
                console.error("Error al obtener información del usuario.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}

function eliminar_zona(id){
    $.ajax({
        url: "/eliminar_zona/" + id,
        type: "GET",
        success: function(response) {
            if (response.success) {
                
                console.log("Zona eliminada exitosamente.");
            } else {
                console.error("Error al eliminar una zona.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}


function get_data_zona(id) {
    $.ajax({
        url: "/get_zona_info/" + id,
        type: "GET",
        success: function(response) {
            console.log("Respuesta completa del servidor:", response);

            if (response.success) {
                var datos_zona = response.zona;
                $("#id_zn_act").val(datos_zona[0]);
                $("#nombreZona_act").val(datos_zona[1]);
                $("#ubicacionZona_act").val(datos_zona[2]);

                var selectAct = datos_zona[3].toString();
                $("#activoZona_act").val(selectAct);  // No es necesario convertir a minúsculas

                

                $("#selectUsuario_act").val(datos_zona[4]);

                $("#modalActualizarZona").modal("show");

            } else {
                console.error("Error al obtener información de la zona.");
            }
        },
        error: function(error) {
            console.error("Error de solicitud:", error);
        }
    });
}