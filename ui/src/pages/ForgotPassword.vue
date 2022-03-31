<template>
  <q-page class="column">
    <div class="q-gutter-lg all-padding">
      <q-input v-model="email" filled hint="请输入绑定邮箱"> </q-input>

      <div>
        <q-btn
          class="full-width"
          color="white"
          text-color="black"
          label="确认"
          @click="modify"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, reactive, watch } from "vue";
import { getUtils, postUtils, putUtils, patchUtils } from "boot/utils";
import { LocalStorage, SessionStorage } from "quasar";
import { useRouter } from "vue-router";
import { useStore } from "stores/bridge";
import { compress, compressAccurately } from "image-conversion";

export default defineComponent({
  name: "UserPwSettings",

  setup() {
    const store = useStore();
    const username = store.user.username;
    const email = ref();

    return {
      async modify() {
        let res = await postUtils(
          process.env.API + "auth/users/reset_password/",
          {
            email: email.value,
          }
        );
        if (res instanceof Error) {
          alert("此邮箱不存在");
        } else {
          alert("重置密码邮件已发送");
        }
      },
      email,
    };
  },
});
</script>
<!-- <style lang = "scss" scoped>
  @import "../assets/style/common.scss";
</style> -->
