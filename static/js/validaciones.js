function validar(type) {
    if(type == 1){
        var nombre = document.getElementById('nombre').value;
        var apellidoP = document.getElementById('apellidoP').value;
        var apellidoM = document.getElementById('apellidoM').value;
        var alias = document.getElementById('alias').value;
        var email = document.getElementById('email').value;
        var psw = document.getElementById('psw').value;
        var tipoUsuario = document.getElementById('tipoUsuario').value;
        // Verifica que los campos no estén vacíos
        if (!nombre || !apellidoP || !apellidoM || !alias || !email || !psw || !tipoUsuario) {
            Swal.fire({
            icon: 'error',
            title: 'Campos vacíos',
            text: 'Todos los campos son obligatorios',
            });
        
            return false;
        }

    }

    if(type == 2){
        var nombreZona = document.getElementById('nombreZona').value;
        var ubicacionZona = document.getElementById('ubicacionZona').value;

        // Verifica que los campos no estén vacíos
        if (!nombreZona || !ubicacionZona) {
            
            Swal.fire({
                icon: 'error',
                title: 'Campos vacíos',
                text: 'Nombre y Ubicación son obligatorios para la zona',
            });

            return false;
        }
    }
    
  
    
  
    return true;
}
  