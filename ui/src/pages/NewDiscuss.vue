<template>
  <q-page class="column">
    <div class="q-gutter-lg all-padding">
      <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
        <q-input
          v-model="title"
          label=""
          filled
          hint="标题"
          style="font-size: large"
        >
        </q-input>

        <q-editor v-model="editor" min-height="15rem" />
        <div class="row">
          <q-input
            v-model="tag"
            label=""
            hint="添加tag"
            style="font-size: large"
            lazy-rules
            :rules="[(val) => tags.indexOf(val) === -1 || '已有tag']"
          >
          </q-input>
          <q-btn label="添加" color="primary" @click="addTag()" flat />
          <q-chip
            removable
            v-for="(i, index) in tags"
            :key="index"
            v-show="tags.length > 0"
            @remove="removeTag(i)"
            color="primary"
            text-color="white"
            icon="local_offer"
          >
            {{ i }}
          </q-chip>
        </div>
        <div class="row reverse">
          <q-btn label="发布" type="submit" color="primary" />
          <q-btn
            label="重置"
            type="reset"
            color="primary"
            flat
            class="q-ml-sm"
          />
        </div>
      </q-form>
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
import { useQuasar } from "quasar";

export default defineComponent({
  name: "NewDiscuss",

  setup() {
    const store = useStore();
    const $q = useQuasar();
    const editor = ref("");
    const title = ref();
    const tag = ref();
    const tags = ref([]);
    return {
      editor,
      title,
      tag,
      tags,
      removeTag(tag) {
        tags.value.splice(tags.value.indexOf(tag), 1);
      },
      addTag() {
        if (tag.value && tags.value.indexOf(tag.value) === -1) {
          tags.value.push(tag.value);
          tag.value = "";
        }
      },
      async onSubmit() {
        if (!title.value || !editor.value) {
          return $q.notify({
            color: "red-5",
            textColor: "white",
            icon: "warning",
            message: "标题和内容不能为空",
          });
        }

        let res = await postUtils(
          process.env.API + "wu/discuss/",
          {
            title: title.value,
            text: editor.value,
            starter: store.user.username,
            tags: tags.value,
          },
          true
        );
        if (res && !(res instanceof Error)) {
          $q.notify({
            color: "green-4",
            textColor: "white",
            icon: "cloud_done",
            message: "发布成功",
          });
          useRouter().push("/");
        }
      },
      onReset() {
        editor.value = "";
        title.value = null;
        tags.value = null;
      },
    };
  },
});
</script>
<!-- <style lang = "scss" scoped>
  @import "../assets/style/common.scss";
</style> -->
