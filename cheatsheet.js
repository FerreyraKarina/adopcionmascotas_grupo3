import { error } from "node:console";

const usuarios = [
  { _id: 1, nombre: 'Ana', roles: ['admin', 'user'], compras: [100, 200] },
  { _id: 2, nombre: 'Bob', roles: ['user'], compras: [50] },
  {_id: 3, nombre: 'pancho', roles: ['admin'], compras: [50]},
  {_id: 4, nombre: 'luisa', roles: ['usuario'], compras: [50]},
  {_id: 5, nombre: 'clark', roles: ['admin'], compras: [50]}

];
/**metodo para obtener algun dato del objeto o array */
let nombresusuarios = usuarios.map(usuario => usuario.nombre)
console.log(nombresusuarios)
/**metodo para obtener objeto o array que cumpla una condicion */
let admins = usuarios.filter(usuario => usuario.roles.includes("admin"))
console.log(admins)
function vertotaldecompras(){
    let totalgeneral = 0
    usuarios.forEach(usuario =>{
        let totalcomprausuarios = usuario.compras.reduce((a,b) => a+b,0)
        totalgeneral += totalcomprausuarios
        console.log(totalgeneral)
    })

}
vertotaldecompras()





/**funcion asyncrona que busca un nombre de una mascota en la base de datos manejados con try cath para que
 * no rompa por ejemplo si no existe la base de datos o no existe esa mascota creando el error y lanzadolo con
 * throw  el async y el await se usan para funciones que van a tardar un poc en hacer su funcion como ir a buscar
 * info externa y con el await se frena esa linea de codigo pero la aplicacion no se frena esperando que esa
 * funcion termine
 */
async function buscardatos(){
    try{
        const datos = await db.collection('mascotas').findOne({ nombre: 'Manchas' });
        console.log(datos)
        if(!datos){
            throw new Error(`mascota no encontrada`)
        }


    }catch(error){
       console.error(` Error en DB: ${error.message}`);

    }

}
obtenerdatos()