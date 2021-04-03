function deleteit(assignment_ID) {
    response =
    fetch('http://localhost:5001/deleteAssignment/' + assignment_ID,
    {method: "DELETE"})
    .then(response =>response.json())
    .then(data => {
      console.log("oof");
      console.log(":ehhh");
      console.log(data.data);
      if (data.code !== 200) {
          // no book in db
          this.message = data.message;
      } else {
        this.message += data.status;
      }
    })
    .catch(error => {
        // Errors when calling the service; such as network error, 
        // service offline, etc
        console.log(this.message + error);
    });
  }