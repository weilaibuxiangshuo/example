const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  defrou: state => state.user.defrou,
  name: state => state.user.name,
  selectDataState:state=>state.menus.selectDataState,
  allpath:state=>state.user.allpath,
}
export default getters
