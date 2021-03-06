/**
 * InterSystems IRIS FHIRAAS
 * Iris Api to manage tenants
 *
 * OpenAPI spec version: 0.1
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */
import { CspConfig } from './cspConfig';
import { InteropConfig } from './interopConfig';
import { ServiceConfigData } from './serviceConfigData';


export interface Endpoint { 
    name?: string;
    enabled?: boolean;
    service_config_data?: ServiceConfigData;
    csp_config?: CspConfig;
    interop_config?: Array<InteropConfig>;
}
