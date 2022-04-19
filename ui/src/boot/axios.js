import { boot } from "quasar/wrappers";
import axios from "axios";
import qs from "qs";
import { LocalStorage, SessionStorage } from "quasar";
import { useRouter } from "vue-router";
import { refreshToken } from "./utils";

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
// const api = axios.create({ baseURL: "https://api.example.com" });
const get = async (url, restricted = false, data) => {
  if (restricted == true) {
    try {
      let access = LocalStorage.getItem("access");
      if (data) {
        let res = await axios.get(url, {
          params: data,
          headers: { Authorization: "JWT " + access },
        });
        return res;
      } else {
        let res = await axios.get(url, {
          headers: { Authorization: "JWT " + access },
        });
        return res;
      }
    } catch (err) {
      return err;
    }
  }
  if (restricted == false) {
    let res = await axios.get(url);
    return res;
  }
};

const post = async (url, data, token) => {
  try {
    if (token)
      return await axios.post(url, qs.stringify(data), {
        headers: { Authorization: "JWT " + token },
      });
    return await axios.post(url, qs.stringify(data));
  } catch (err) {
    return err;
  }
};
export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api
  // app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file
  // app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

export { get, post };
