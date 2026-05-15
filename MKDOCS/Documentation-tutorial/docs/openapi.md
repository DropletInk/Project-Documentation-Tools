<!-- <redoc spec-url="../openapi.json" ></redoc>

<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>  -->



<swagger-ui src="../openapi.json"></swagger-ui> 

<div id="swagger-ui"></div>

<script>
window.onload = function () {
  SwaggerUIBundle({
    url: "../openapi.json",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    layout: "BaseLayout"
  });
};
</script> 
