Class FHIRAAS.API.spec Extends %REST.Spec [ ProcedureBlock ]
{

XData OpenAPI [ MimeType = application/json ]
{
{
  "swagger": "2.0",
  "info": {
    "title": "Iris Management",
    "description": "Iris Api to manage tenants",
    "version": "1.0.0"
  },
  "host": "api.fhir.fr",
  "basePath": "/v1/management/",
  "schemes": [
    "https"
  ],
  "paths": {
    "/tenants": {
      "get": {
        "summary": "Returns a list of tenants.",
        "operationId": "getTenants",
        "description": "Return the list of available tenant on this Iris instance.",
        "produces": [
          "application/json"
        ],
        "responses": {
          "200": {
            "description": "OK"
          }
        }
      }
    },
    "/tenants/{tenantId}": {
      "get": {
        "summary": "Returns a tenant by ID.",
        "operationId": "getTenant",
        "parameters": [
          {
            "in": "path",
            "name": "tenantId",
            "required": true,
            "type": "string",
            "description": "the tenant Id"
          }
        ],
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "Not Found"
          }
        }
      },
      "put": {
        "summary": "Create a tenant with an ID.",
        "operationId": "putTenant",
        "parameters": [
          {
            "in": "path",
            "name": "tenantId",
            "required": true,
            "type": "string",
            "description": "the tenant Id"
          },
          {
            "in": "body",
            "name": "tenantInformations",
            "schema": {
              "$ref": "#/definitions/CreateTenant"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "Not Found"
          },
          "500": {
            "description": "Server error"
          }
        }
      },
      "delete": {
        "summary": "Delete a tenant with an ID.",
        "operationId": "deleteTenant",
        "parameters": [
          {
            "in": "path",
            "name": "tenantId",
            "required": true,
            "type": "string",
            "description": "the tenant Id"
          }
        ],
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "Not Found"
          },
          "500": {
            "description": "Server error"
          }
        }
      }
    },
    "/tenants/{tenantId}/{endpointId}": {
      "get": {
        "summary": "Returns a tenant by ID.",
        "operationId": "getEndpoint",
        "parameters": [
          {
            "in": "path",
            "name": "tenantId",
            "required": true,
            "type": "string",
            "description": "the tenant Id"
          },
          {
            "in": "path",
            "name": "endpointId",
            "required": true,
            "type": "string",
            "description": "the endpoint Id"
          }
        ],
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "Not Found"
          }
        }
      },
      "put": {
        "summary": "Create a endpoint with an ID.",
        "operationId": "putEndpoint",
        "parameters": [
          {
            "in": "path",
            "name": "tenantId",
            "required": true,
            "type": "string",
            "description": "the tenant Id"
          },
          {
            "in": "path",
            "name": "endpointId",
            "required": true,
            "type": "string",
            "description": "the endpoint Id"
          },
          {
            "in": "body",
            "name": "tenantInformations",
            "schema": {
              "$ref": "#/definitions/CreateTenant"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "Not Found"
          },
          "500": {
            "description": "Server error"
          }
        }
      },
      "delete": {
        "summary": "Delete a endpoint with an ID.",
        "operationId": "deleteEndpoint",
        "parameters": [
          {
            "in": "path",
            "name": "tenantId",
            "required": true,
            "type": "string",
            "description": "the tenant Id"
          },
          {
            "in": "path",
            "name": "endpointId",
            "required": true,
            "type": "string",
            "description": "the endpoint Id"
          }
        ],
        "responses": {
          "200": {
            "description": "OK"
          },
          "404": {
            "description": "Not Found"
          },
          "500": {
            "description": "Server error"
          }
        }
      }
    }
  },
  "definitions": {
    "CreateTenant": {
      "type": "object",
      "properties": {
        "rootPassword": {
          "type": "string"
        }
      }
    },
    "Tenant": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string"
        },
        "status": {
          "type": "string"
        }
      },
      "required": [
        "id"
      ]
    }
  }
}
}

}
