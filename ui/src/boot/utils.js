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
  authValid = async (data, raw) => {
    if (!(data instanceof Error)) return data;
    // console.log("data", data.request);

    if (data.response.status === 401) {
      const res = await refreshToken();

      if (!res) {
        alert("登陆已过期");
        LocalStorage.remove("access");
        LocalStorage.remove("refresh");
        redirect({
          path: "/auth",
        });
        return null;
      } else {
        return postUtils(data.request.responseURL, raw, true);
      }
    }
  };
  getUtils = async (url, restricted, data) => {
    if (data) {
      const res = await get(url, restricted, data);
      return authValid(res);
    }
    const res = await get(url, restricted);
    return authValid(res);
  };
  postUtils = async (url, data, restricted) => {
    if (restricted) {
      let access = LocalStorage.getItem("access");
      const res = await post(url, data, access);
      return authValid(res, data);
    }
    const res = await post(url, data);
    return authValid(res, data);
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

    if (!refreshRes.data) return false;
    LocalStorage.set("access", refreshRes.data.access);
    LocalStorage.set("refresh", refreshRes.data.refresh);
    return refreshRes;
  };
});

export { getUtils, postUtils, putUtils, patchUtils, refreshToken };
