<template>
  <q-page class="column">
    <div class="q-gutter-lg all-padding">
      <q-input v-model="email" filled hint="请输入新邮箱"> </q-input>

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
  name: "UserEmailSettings",

  setup() {
    const store = useStore();
    const username = store.user.username;
    const email = ref();

    return {
      async modify() {
        let res = await postUtils(process.env.API + "wu/changeemail/", {
          username: username,
          email: email.value,
        });
        if (res instanceof Error) {
          alert(res.response.data);
        } else {
          alert(res.data);
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
