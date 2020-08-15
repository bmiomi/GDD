function beta(e) {
  let ipAPI = 'http://127.0.0.1:5000/rutas'
  Swal.fire(
    {
      title: 'Revisando GDD',
      confirmButtonText: 'Aceptar',
      text: 'Mostrar informe de GDD para el DZ ' + e.id,
      showLoaderOnConfirm: true,
      preConfirm: () => {
        return fetch(ipAPI, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ name: e.id })

        })
          .then(response => {
            if (!response.ok) {
              throw new Error(response.statusText)
            }
            return response.json()
          })
          .catch((error) => {
            Swal.showValidationMessage(
              `Se Produjo un error al realizar una peticion con el servidor verificar : ${error}`
            )
          })
      },
      allowOutsideClick: () => !Swal.isLoading()
    })

    .then(result => {
      console.log(result.value.status);
      if (result.value.status === "OK") {
        Swal.fire({
          icon: 'success',
          title: `${result.value.message} `,
        })
      } else if (result.value.status === "ERROR") {
        Swal.fire({
          icon: 'warning',
          title: `${result.value.message} `,
        })
      } else if (result.value.status === "Info") {
        Swal.fire({
          icon: 'Info',
          title: `${result.value.message} `,
        })
      }


    })



}