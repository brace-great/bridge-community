import { get, post } from "./axios";
import axios from "axios";
import { boot } from "quasar/wrappers";
import { LocalStorage, SessionStorage } from "quasar";

let authValid;
let getUtils;
let postUtils;
let putUtils;
let patchUtils;
let refreshToken;
export default boot(({ redirect }) => {
  authValid = async (data) => {
    if (!data) {
      const res = await refreshToken();
      if (!res) {
        alert("登陆已过期");
        LocalStorage.remove("access");
        LocalStorage.remove("refresh");
        redirect({
          path: "/auth",
        });
        return null;
      }
    }
    return data;
  };
  getUtils = async (url, restricted) => {
    const res = await get(url, restricted);
    return authValid(res);
  };
  postUtils = async (url, data, restricted) => {
    if (restricted) {
      let access = LocalStorage.getItem("access");
      const res = await post(url, data, access);
      return authValid(res);
    }
    const res = await post(url, data);
    return authValid(res);
  };
  putUtils = async (url, data) => {
    let access = LocalStorage.getItem("access");
    const res = await axios.put(url, data, {
      // params: data.data,
      headers: { Authorization: "JWT " + access },
    });
    return authValid(res);
  };
  patchUtils = async (url, data) => {
    let access = LocalStorage.getItem("access");
    const res = await axios.patch(url, data, {
      // params: data.data,
      headers: { Authorization: "JWT " + access },
    });
    return authValid(res);
  };
  refreshToken = async () => {
    let refresh = LocalStorage.getItem("refresh");
    let refreshRes = await post(
      process.env.API + "auth/jwt/refresh/",
      { refresh: refresh },
      refresh
    );
    LocalStorage.set("access", refreshRes.data.access);
    LocalStorage.set("refresh", refreshRes.data.refresh);
    return refreshRes;
  };
});

export { getUtils, postUtils, putUtils, patchUtils, refreshToken };
