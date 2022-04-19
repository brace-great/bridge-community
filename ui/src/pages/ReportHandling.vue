<template>
  <q-page class="column">
    <q-list style="padding-top: 5px" separator class="content-center">
      <q-item v-for="(i, index) in reportData" :key="index">
        <q-item-section>
          <q-item-label
            style="font-size: large"
            class="row items-center justify-between"
            >用户{{ i.reporter }}举报了用户{{ i.username }}的{{
              i.content_type == "comment" ? "评论" : "讨论"
            }},理由为{{ i.reason }},原文为:
          </q-item-label>
          <q-item-label caption :lines="lines[index]">
            {{ i.content_text }}
          </q-item-label>
        </q-item-section>

        <q-item-section side top class="column">
          <q-item-label caption>{{ i.time }}</q-item-label>
          <div>
            <q-btn
              label="展开"
              color="primary"
              style="margin-top: 15px"
              @click="expand(index)"
              v-show="lines[index] == 3"
            />
            <q-btn
              label="确认撤回"
              @click="
                confirmWithdrawal(i.id, i.content_type, i.content_id, true)
              "
              color="primary"
              style="margin-top: 15px"
            />
            <q-btn
              label="忽略此举报"
              @click="
                confirmWithdrawal(i.id, i.content_type, i.content_id, false)
              "
              color="primary"
              style="margin-top: 15px"
            />
          </div>
          <q-btn
            label="收回"
            color="primary"
            style="margin-top: 15px"
            @click="reclaim(index)"
            v-show="lines[index] != 3"
          />
          <q-btn
            label="收回"
            color="primary"
            style="margin-top: auto"
            @click="reclaim(index)"
            v-show="lines[index] != 3"
          />
        </q-item-section>
      </q-item>

      <q-separator spaced inset="item" />
    </q-list>
  </q-page>
</template>

<script>
import { defineComponent, onBeforeMount, ref, reactive, watch } from "vue";
import {
  getUtils,
  postUtils,
  putUtils,
  patchUtils,
  deleteUtils,
} from "boot/utils";
import { LocalStorage, SessionStorage } from "quasar";
import { useRouter } from "vue-router";
import { useStore } from "stores/bridge";
import { compress, compressAccurately } from "image-conversion";
import { useQuasar } from "quasar";

export default defineComponent({
  name: "ReportHandling",

  setup() {
    const store = useStore();
    const reportData = ref();
    const lines = ref([]);
    const $q = useQuasar();

    onBeforeMount(async () => {
      const res = await getUtils(process.env.API + "wu/report/", true);
      reportData.value = res.data.results;
      for (const i in reportData.value) {
        lines.value[i] = 3;
      }
    });
    return {
      reportData,
      lines,
      async confirmWithdrawal(id, content_type, content_id, is_withdraw) {
        let res;
        if (!is_withdraw) {
          res = await deleteUtils(process.env.API + "wu/report/" + id + "/");
          if (res.status == 204) {
            $q.notify({
              color: "positive",
              textColor: "white",
              message: "已忽略",
            });
          } else {
            $q.notify({
              color: "negative",
              textColor: "white",
              message: "未知错误",
            });
          }
        } else {
          if (content_type == "comment") {
            res = await patchUtils(
              process.env.API + "wu/comment/" + content_id + "/",
              {
                notshow: 1,
              }
            );
          } else {
            res = await patchUtils(
              process.env.API + "wu/discuss/" + content_id + "/",
              {
                isshow: 0,
              }
            );
          }
          if (res.status == 200) {
            $q.notify({
              color: "positive",
              textColor: "white",
              message: "撤回成功",
            });
          } else {
            $q.notify({
              color: "negative",
              textColor: "white",
              message: "未知错误",
            });
          }
          res = await deleteUtils(process.env.API + "wu/report/" + id + "/");
        }
        const resRefresh = await getUtils(process.env.API + "wu/report/", true);
        reportData.value = resRefresh.data.results;
      },

      expand(index) {
        lines.value[index] = "";
      },
      reclaim(index) {
        lines.value[index] = 3;
      },
      store,
    };
  },
});
</script>
<!-- <style lang = "scss" scoped>
  @import "../assets/style/common.scss";
</style> -->
