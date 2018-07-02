getLocation () {
  
  if (!navigator.geolocation){
    return swal('您的浏览器不支持位置信息');
  }
  function success(position) {
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;

  }
  function error() {
    swal('无法获取您的位置')
  };
  navigator.geolocation.getCurrentPosition((position)=>{
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;
    this.location = latitude + ',' + longitude
  }, error);
}

