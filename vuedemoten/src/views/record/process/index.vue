<template>
  <div id="databox">
    <div class="dataheader">
      <!-- <div class="firstheader"></div> -->
      <!-- 添加及搜索 -->
      <div class="secondheader" style="width:100%">
        <el-form :rules="rules" ref="headerForm" :inline="true" class="demo-ruleForm">
          <el-form-item label="所属日期" class="timeStyle">
            <el-date-picker
              :disabled="boolStatus"
              type="date"
              placeholder="选择日期"
              v-model="timeChange"
              value-format="yyyy-MM-dd"
              format="yyyy-MM-dd"
              :picker-options="pickerOptions"
              @change="timePutChange"
            >></el-date-picker>
          </el-form-item>
          <el-form-item >
            <el-select
              v-model.trim="refresh"
              placeholder="自动刷新"
              style="width:120px;"
              clearable
              @change="changeMethod"
            >
              <el-option label="10秒" value="10"></el-option>
              <el-option label="20秒" value="20"></el-option>
              <el-option label="30秒" value="30"></el-option>
              <el-option label="60秒" value="60"></el-option>
            </el-select>
            <el-select
              v-model.trim="filterDisplay"
              placeholder="筛选显示"
              style="width:120px;"
              clearable
              @change="filterMethod"
            >
              <el-option label="未锁定" value="1"></el-option>
              <el-option label="已锁定" value="2"></el-option>
              <el-option label="未确定" value="3"></el-option>
              <el-option label="已确定" value="4"></el-option>
              <el-option label="自锁定" value="5"></el-option>
              <el-option label="自确定" value="6"></el-option>
            </el-select>

          </el-form-item>
          <el-form-item>
            <el-button
              icon="el-icon-refresh-left"
              type="primary"
              plain
              @click.native.prevent="refreshBtnShow"
            ></el-button>
          </el-form-item>
          <el-form-item>
            <el-input
              placeholder="请输入内容"
              v-model.trim="searchContext"
              class="input-with-select"
              style="width:600px"
              clearable
              @change="serchPutChange"
            >
              <el-select v-model="searchData" slot="prepend" placeholder="请选择" style="width:150px">
                <el-option label="订单号" value="1"></el-option>
                <el-option label="会员账号" value="2"></el-option>
                <el-option label="真实姓名" value="3"></el-option>
                <el-option label="对应金额" value="4"></el-option>
                <el-option label="银行卡号" value="5"></el-option>
              </el-select>
              <el-button
                slot="append"
                icon="el-icon-search"
                class="searchIconStyle"
                @click.native.prevent="searchBtnControl"
              ></el-button>
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <hr />
    </div>

    <div class="datamain">
      <!-- 弹窗对话框  -->
      <el-dialog
        title="提交失败的订单号"
        :visible.sync="dialogFormVisible"
        :before-close="handleClose"
        :close-on-click-modal="false"
        width="550px"
      >
        <el-form :model="dialogform" ref="ruleForm" :rules="rules">
          <el-form-item
            label="订单号"
            :label-width="formLabelWidth"
            prop="onlyid"
            class="amountStyle"
          >
            <el-input
              v-model.trim="dialogform.onlyid"
              autocomplete="off"
              clearable
              placeholder="请输入订单号"
            ></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click.native.prevent="cancel">取 消</el-button>
          <el-button type="primary" @click.native.prevent="confirm">确 定</el-button>
        </div>
      </el-dialog>

      <!-- 表格渲染 -->
      <el-table ref="tableForm" :data="tableData" style="width: 100%" border>
        <el-table-column label="日期" prop="date_group" fixed width="50px">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>{{ scope.row.date_group }}</p>
              <div slot="reference" class="name-wrapper" style="text-align:center">
                <i class="el-icon-time"></i>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="订单号" prop="onlyid" fixed width="80px">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>{{ scope.row.onlyid }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium">单号</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="真实姓名" prop="name" width="150px">
          <template slot-scope="scope">
            <div v-if="scope.row.remark!==''">
              <el-popover trigger="hover" placement="top">
                <p>备注：{{ scope.row.remark }}</p>
                <div slot="reference" class="name-wrapper">
                  <div
                    style="color:#3c0ef7"
                  >{{ scope.row.is_lock && scope.row.is_if_show?scope.row.name:scope.row.name.substr(0,3)+"***" }}</div>
                </div>
              </el-popover>
            </div>
            <div
              v-else
            >{{ scope.row.is_lock && scope.row.is_if_show?scope.row.name:scope.row.name.substr(0,3)+"***" }}</div>
          </template>
        </el-table-column>
        <el-table-column label="对应金额" prop="amount" width="150px">
          <!-- <template v-slot="scope">
            <div>{{scope.row.is_freeze && scope.row.is_if_show?scope.row.amount:"***"}}</div>
          </template>-->
        </el-table-column>
        <el-table-column label="所属银行" prop="cardclass" width="200px">
          <template v-slot="scope">
            <div>{{scope.row.is_lock && scope.row.is_if_show?scope.row.cardclass:scope.row.cardclass.substr(0,3)+"***"}}</div>
          </template>
        </el-table-column>
        <el-table-column label="银行卡号" prop="cardnum" width="200px">
          <template v-slot="scope">
            <div>{{(scope.row.is_lock && scope.row.is_if_show)?scope.row.cardnum:scope.row.cardnum.substr(0,3)+"***"}}</div>
          </template>
        </el-table-column>
        <el-table-column label="会员账号" prop="account" width="150px"></el-table-column>
        <el-table-column label="操作者" prop="operator" width="150px"></el-table-column>
        <el-table-column label="所属用户" prop="user_group" width="150px"></el-table-column>
        <el-table-column align="left" label="操作" fixed="right" width="200px">
          <template v-slot="scope">
            <div v-if="!scope.row.is_confirm">
              <div v-if="scope.row.is_if_show && !scope.row.is_freeze">
                <el-button
                  size="mini"
                  :type="scope.row.is_lock?'info':'primary'"
                  :disabled="scope.row.is_confirm"
                  @click="handleStatus(scope.$index, scope.row,scope.row.is_lock)"
                >
                  {{scope.row.is_lock?'解锁':'锁定'}}
                  <i
                    class="el-icon--right"
                    :class="scope.row.is_lock?'el-icon-lock':'el-icon-unlock'"
                  ></i>
                </el-button>
                <el-button
                  size="mini"
                  :type="scope.row.is_confirm?'info':'warning'"
                  :disabled="!scope.row.is_lock"
                  @click="handleConfirm(scope.$index, scope.row)"
                >确定</el-button>
              </div>
              <div v-else>
                <i class="el-icon--right el-icon-loading"></i>
                数据处理中......
              </div>
            </div>
            <div v-else>
              <i class="el-icon--right el-icon-success"></i>
              已完成受理
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 分页及按钮 -->
    <div class="datafooter">
      <div class="btnStyle">
        <el-input
          v-model="totalSum"
          style="width:300px;vertical-align: top;color:#4d58dc;"
          size="small"
          class="totalSumStyle"
        >
          <template slot="prepend">总计：</template>
        </el-input>
        <el-input v-model="smallSum" style="width:300px;vertical-align: top;" size="small">
          <template slot="prepend">小计：</template>
        </el-input>
        <el-button
          type="danger"
          icon="el-icon-warning"
          size="small"
          @click.native.prevent="failrecord"
        >提交失败单号</el-button>
      </div>
      <div class="paginationStyle">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagin.currentPage"
          :page-sizes="pagin.pagesizes"
          :page-size="pagin.pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagin.total"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>
<script>
// 弹窗对话框初始值
const defaultDialogForm = {
  onlyid: "",
};

// 分页初始值
const defaultPagin = {
  currentPage: 1,
  pagesizes: [10, 20, 50],
  pagesize: 10,
  total: 0,
};

export default {
  data() {
    const onlyidVali = (rule, value, callback) => {

      const strVal = value.toString();
      if (strVal.length === 0) {
        return callback(new Error("请输入订单号"));
      }
      const regTemp = /^[0-9A-Za-z]+$/;
      const res = strVal.match(regTemp);
      if (!res) {
        return callback(new Error("订单号禁含有非数字或字母符号"));
      }
      return callback();
    };
    return {
      // -----------添加及搜索-----------
      filterDisplay: "",
      refresh: "",
      autoRefresh: "",
      searchData: "",
      searchSetData: [],
      searchContext: "",
      paramsdict: {},
      timeChange: "",
      boolStatus: false,
      pickerOptions: {
        // disabledDate(time) {
        //   return time.getTime() + 3600 * 1000 * 24 * 16 < Date.now();
        // },
        shortcuts: [
          {
            text: "今天",
            onClick(picker) {
              picker.$emit("pick", new Date());
            },
          },
          {
            text: "昨天",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit("pick", date);
            },
          },
          {
            text: "一周前",
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", date);
            },
          },
        ],
      },
      // ----------- 弹窗对话框-----------
      dialogFormVisible: false,
      dialogform: Object.assign({}, defaultDialogForm),
      formLabelWidth: "80px",
      // ----------- 表格渲染-----------
      is_show_btn: true,
      tableData: [],
      isActiveFreeze: true,
      // ----------- 分页-----------
      totalSum: "",
      smallSum: "",
      pagin: Object.assign({}, defaultPagin),
      // ----------- 验证-----------
      rules: {
        onlyid: [{ required: true, validator: onlyidVali, trigger: "blur" }],
      },
    };
  },
  methods: {
    // -----------添加及搜索-----------
    timePutChange(val) {
      this.pagin.currentPage = 1;
      this.boolStatus = true;
      this.getAllInfo();
    },

    // 筛选显示
    filterMethod(val) {
      if (!!this.timeChange) {
        this.pagin.currentPage = 1;
        this.getAllInfo();
      } else {
        this.filterDisplay = "";
        const h = this.$createElement;
        this.$notify({
          message: h(
            "b",
            { style: "color: #ef9206" },
            "请先选择-所属日期，才能自动刷新"
          ),
          duration: 2000,
        });
        return false;
      }
    },
    // 刷新
    changeMethod(val) {
      if (!!this.timeChange) {
        if (val === "") {
          clearInterval(this.autoRefresh);
          return false;
        }
        clearInterval(this.autoRefresh);
        const valInt = parseInt(val) * 1000;
        this.autoRefresh = setInterval(this.getAllInfo, valInt);
      } else {
        this.refresh = "";
        const h = this.$createElement;
        this.$notify({
          message: h(
            "b",
            { style: "color: #ef9206" },
            "请先选择-所属日期，才能自动刷新"
          ),
          duration: 2000,
        });
        return false;
      }
    },
    // 搜索框没有值时触发
    serchPutChange(val) {
      let newVal = val.toString().trim();
      if (newVal == "") {
        this.pagin.currentPage = 1;
        this.getAllInfo();
      } else {
        return false;
      }
    },
    // 按下搜索时触发
    searchBtnControl() {
      if (!!this.searchData && !!this.searchContext && !!this.timeChange) {
        this.pagin.currentPage = 1;
        this.getAllInfo();
      } else {
        const h = this.$createElement;
        if (!this.timeChange) {
          this.$notify({
            message: h(
              "b",
              { style: "color: #ef9206" },
              "请先选择-所属日期，才能操作"
            ),
            duration: 2000,
          });
        } else if (!this.searchData) {
          this.$notify({
            message: h(
              "b",
              { style: "color: #ef9206" },
              "请先选择-搜索项目，才能操作"
            ),
            duration: 2000,
          });
        } else if (!this.searchContext) {
          this.$notify({
            message: h(
              "b",
              { style: "color: #ef9206" },
              "请输入搜索内容，才能操作"
            ),
            duration: 2000,
          });
        }
        return false;
      }
    },
    // ----------- 弹窗对话框-----------
    //点击对话框外面事件
    handleClose(done) {
      this.dialogFormVisible = false;
      this.$refs["ruleForm"].resetFields();
      done();
      return false;
    },
    // 确定送出
    confirm() {
      this.$refs["ruleForm"].validate((val) => {
        if (val) {
          this.dialogFormVisible = false;
          let newInfo = this.dialogform;
          newInfo["timeinfo"] = this.timeChange;
          let reqData = JSON.stringify(newInfo);
            this.$store
              .dispatch("process/AddEventprocessFail", reqData)
              .then((response) => {
                this.getAllInfo();
                const { code, msg } = response;
                this.$message({
                  type:
                    code.toString().substr(0, 1) === "2" ? "success" : "error",
                  message: msg,
                });
              });
        }
      });
    },
    // 取消对话框
    cancel() {
      this.dialogFormVisible = false;
      this.$refs["ruleForm"].resetFields();
    },
    // ----------- 表格渲染-----------
    // 获取所有目标
    getAllInfo() {
      this.paramsdict = Object.assign({}, {});
      if (!this.timeChange) {
        return false;
      } else {
        this.paramsdict["timeinfo"] = this.timeChange;
      }
      if (!!this.searchData && !!this.searchContext) {
        this.paramsdict["searchgroup"] = this.searchData;
        this.paramsdict["searchcontext"] = this.searchContext;
      }
      if (!!this.filterDisplay) {
        this.paramsdict["filterdisplay"] = this.filterDisplay;
      }
      if (
        (this.pagin.currentPage - 1) * this.pagin.pagesize ==
          this.pagin.total &&
        this.pagin.currentPage - 1 > 0
      ) {
        this.pagin.currentPage -= 1;
      }
      let dataInfo = {
        currentpage:
          this.pagin.currentPage === null ? 1 : this.pagin.currentPage,
        pagesize: this.pagin.pagesize,
      };

      if (!!this.paramsdict) {
        dataInfo["search"] = this.paramsdict;
      }
      this.$store
        .dispatch("process/GetEventprocess", dataInfo)
        .then((response) => {
          const { data, total, sum } = response;
          this.tableData = data;
          this.pagin.total = total;
          this.totalSum = sum;
          if (response.data.length > 0) {
            let items = response.data;
            let smallSum = 0;
            for (let i in items) {
              smallSum += items[i].amount;
            }
            this.smallSum = smallSum;
          } else {
            this.smallSum = "";
          }
        });
    },
    // 按钮确定
    handleConfirm(index, row) {
      // this.is_show_btn = false;
      if (!row.is_lock) {
        return false;
      }

      let data = {
        id: row.id,
        onlyid: row.onlyid,
      };
      this.$store
        .dispatch("process/EventprocessConfirm", data)
        .then((response) => {
          const { code, msg } = response;
          if (code.toString().substr(0, 1) === "2") {
            row.is_confirm = !row.is_confirm;
          }
          this.$message({
            type: code.toString().substr(0, 1) === "2" ? "success" : "error",
            message: msg,
          });
        });
    },
    // 锁定
    handleStatus(index, row, sccc) {
      let data = {
        id: row.id,
        onlyid: row.onlyid,
        is_lock: !sccc,
      };
      this.$store
        .dispatch("process/EventprocessStatus", data)
        .then((response) => {
          const { code, msg } = response;
          if (code.toString().substr(0, 1) === "2") {
            this.getAllInfo();
          }
          this.$message({
            type: code.toString().substr(0, 1) === "2" ? "success" : "error",
            message: msg,
          });
        });
    },
    // ----------- 分页-----------
    // 提交失败订单
    failrecord() {
      this.dialogFormVisible = true;
    },
    // 当前一页显示数量
    handleSizeChange(val) {
      let isR = val * this.pagin.currentPage > this.pagin.total;
      if (isR) {
        this.pagin.pagesize = val;
        this.handleCurrentChange(1);
        return false;
      }
      this.pagin.pagesize = val;
      this.getAllInfo();
    },
    // 当前页码
    handleCurrentChange(val) {
      this.pagin.currentPage = val;
      this.getAllInfo();
    },
  },
  created() {
    // this.getAllInfo();
  },
};
</script>
<style scoped>
.dataheader {
  margin-top: 10px;
}
.datamain {
  margin-left: 22px;
}

.timeStyle /deep/ .el-form-item__label,
.timeStyle /deep/ .el-input__inner {
  color: #077bf3;
}

.timeStyle >>> .el-form-item__label,
.timeStyle >>> .el-input__inner {
  color: #077bf3;
}

.secondheader {
  margin-left: 20px;
}

.searchIconStyle {
  margin: auto 0;
}

.amountStyle /deep/ .el-form-item__label,
.amountStyle /deep/ .el-input__inner {
  color:#F56C6C;
}
.amountStyle >>> .el-form-item__label,
.amountStyle >>> .el-input__inner {
  color: #F56C6C;
}

.totalSumStyle /deep/ .el-input-group__prepend,
.totalSumStyle /deep/ .el-input__inner {
  color: #ca8347;
}
.totalSumStyle >>> .el-input-group__prepend,
.totalSumStyle >>> .el-input__inner {
  color: #ca8347;
}

.msgheader {
  display: inline-block;
  margin-left: 30px;
}
.msgheader span:nth-child(2) {
  margin-left: 10px;
  color: red;
}
.msgheader span:last-child {
  margin-left: 10px;
}
.btnStyle {
  margin-top: 20px;
  margin-left: 30px;
  vertical-align: middle;
}

.paginationStyle {
  margin-top: 20px;
  margin-left: 30px;
  display: inline-block;
  vertical-align: middle;
}

.btnDelStyle {
  background-color: #f56c6c;
  border-color: #f56c6c;
}

.spstyle {
  margin-right: 61px;
}
</style>