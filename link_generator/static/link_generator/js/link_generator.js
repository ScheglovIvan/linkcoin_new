document.addEventListener('DOMContentLoaded', function() {
  const FIELDS = document.getElementsByClassName('field-__str__');

  const PROTOCOL = window.location.protocol;
  const HOST = window.location.host;

  for (const FIELD of FIELDS) {
    const LINK = FIELD.getElementsByTagName('a')[0];
    LINK.innerHTML = `${PROTOCOL}//${HOST}/register?link=${LINK.innerHTML}`;
  }

});
