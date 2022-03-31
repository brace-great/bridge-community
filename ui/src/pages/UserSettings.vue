<template>
  <q-page class="column">
    <div class="q-gutter-lg all-padding">
      <q-avatar size="100px" class="offset-1">
        <img :src="avatar" />
      </q-avatar>
      <q-input
        @update:model-value="
          (val) => {
            file = val[0];
          }
        "
        filled
        type="file"
        hint="修改头像(大小100 * 100像素,支持JPG、PNG等格式,大小不超过1M)"
      />
      <q-input outlined v-model="introduce" hint="简介" :dense="dense" />
      <div>
        <q-btn
          color="white"
          text-color="black"
          label="修改密码"
          to="password"
          style="margin-right: 10px"
        />
        <q-btn color="white" text-color="black" label="修改邮箱" to="email" />
      </div>

      <q-input v-model="email" filled type="email" hint="Email" readonly />
      <q-input v-model="date" filled type="date" hint="生日" />
      <div>
        <q-btn
          class="full-width"
          color="white"
          text-color="black"
          label="保存"
          @click="modify"
        />
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, reactive, watch } from "vue";
import { getUtils, postUtils, putUtils } from "boot/utils";
import { LocalStorage, SessionStorage } from "quasar";
import { useRouter } from "vue-router";
import { useStore } from "stores/bridge";
import { compress, compressAccurately } from "image-conversion";

export default defineComponent({
  name: "UserSettings",

  setup() {
    const avatar = ref();
    const introduce = ref();
    const email = ref();
    const date = ref();
    const store = useStore();
    const username = store.user.username;
    const file = ref();

    getUtils(process.env.API + "wu/userinfos/" + username, true).then((res) => {
      email.value = res.data.email;
      avatar.value = res.data.avatar;
      introduce.value = res.data.introduce;
      date.value = res.data.birthday;
    });
    const test = "gg";
    watch(file, () => {
      var reader = new FileReader();
      compressAccurately(file.value, 20).then((res) => {
        let rawImg;
        reader.onloadend = () => {
          rawImg = reader.result;
          avatar.value = rawImg;
        };
        reader.readAsDataURL(res);
      });
    });
    return {
      modify() {
        putUtils(process.env.API + "wu/userinfos/" + username + "/", {
          username,
          email: email.value,
          introduce: introduce.value,
          birthday: date.value,
          avatar: avatar.value,
        })
          .then((res) => {
            if (res) {
              alert("修改成功");
            }
          })
          .catch((err) => {
            alert("修改失败,错误信息:" + JSON.stringify(err.response.data));
          });
      },
      test,
      avatar: avatar,
      introduce: introduce,
      email: email,
      file: file,
      date: date,
    };
  },
});
</script>
<!-- <style lang="scss" scoped>
  @import "../assets/style/common.scss";
</style> -->
