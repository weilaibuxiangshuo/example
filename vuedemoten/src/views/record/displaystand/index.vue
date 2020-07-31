<template>
  <div id="databox">
    <div class="dataheader">
      <!-- <div class="firstheader"></div> -->
      <!-- 添加及搜索 -->
      <div class="secondheader" style="width:100%">
        <el-form ref="headerForm" :inline="true" class="demo-ruleForm">
          <el-form-item label="所属日期" class="timeStyle">
            <el-date-picker
              :disabled="boolStatus"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              placeholder="选择日期"
              v-model="timeChange"
              value-format="yyyy-MM-dd"
              format="yyyy-MM-dd"
              :picker-options="pickerOptions"
              @change="timePutChange"
            ></el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-select
              v-model.trim="filterDisplay"
              placeholder="筛选显示"
              style="width:120px;"
              clearable
              @change="filterMethod"
            >
              <el-option label="成功订单" value="1"></el-option>
              <el-option label="失败订单" value="2"></el-option>
            </el-select>
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
                <el-option label="操作者" value="6"></el-option>
                <el-option label="所属用户" value="7"></el-option>
                <el-option label="备注" value="8"></el-option>
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
      <!-- 表格渲染 -->
      <el-table ref="tableForm" :data="tableData" style="width: 100%" border>
        <el-table-column type="selection" width="40px" v-dataBtnControl="this.$route"></el-table-column>
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
        <el-table-column label="状态" prop="is_confirm" width="50px">
          <template v-slot="scope">
            <div v-if="scope.row.is_confirm" style="text-align: center;">
              <i class="el-icon-success"></i>
            </div>
            <div v-else>
              <i class="el-icon-error"></i>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="会员账号" prop="account" width="150px">
          <template v-slot="scope">
            <div v-if="!!scope.row.spare1">
              <el-popover trigger="hover" placement="top">
                <p>提交者：{{ scope.row.spare1 }}</p>
                <div slot="reference" class="name-wrapper">
                  <div style="color:red">{{ scope.row.account}}</div>
                </div>
              </el-popover>
            </div>
            <div v-else>{{scope.row.account}}</div>
          </template>
        </el-table-column>
        <el-table-column label="真实姓名" prop="name" width="150px"></el-table-column>
        <el-table-column label="对应金额" prop="amount" width="150px"></el-table-column>
        <el-table-column label="所属银行" prop="cardclass" width="200px"></el-table-column>
        <el-table-column label="银行卡号" prop="cardnum" width="200px"></el-table-column>

        <el-table-column label="操作者" prop="operator" width="150px"></el-table-column>
        <el-table-column label="所属用户" prop="user_group" width="150px"></el-table-column>
        <el-table-column label="备注" prop="remark" width="200px"></el-table-column>
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
      </div>
      <div class="paginationStyle">
        <el-button type="primary" icon="el-icon-share" @click="selectAllData" size="mini" v-dataBtnControl="this.$route">全选</el-button>
        <el-button
          type="primary"
          icon="el-icon-delete"
          class="btnDelStyle"
          @click="delAllData"
          size="mini"
          v-dataBtnControl="this.$route"
        >全删</el-button>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagin.currentPage"
          :page-sizes="pagin.pagesizes"
          :page-size="pagin.pagesize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagin.total"
          style="display: inline-block;"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>
<script>
// 分页初始值
const defaultPagin = {
  currentPage: 1,
  pagesizes: [10, 20, 50],
  pagesize: 10,
  total: 0,
};

export default {
  data() {
    return {
      // -----------添加及搜索-----------
      filterDisplay: "",
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
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "最近三个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
      // ----------- 表格渲染-----------
      is_show_btn: true,
      tableData: [],
      isActiveFreeze: true,
      // ----------- 分页-----------
      totalSum: "",
      smallSum: "",
      pagin: Object.assign({}, defaultPagin),
    };
  },
  methods: {
    // -----------添加及搜索-----------
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
    timePutChange(val) {
      this.pagin.currentPage = 1;
      this.getAllInfo();
    },
    // ----------- 弹窗对话框-----------
    //点击对话框外面事件
    handleClose(done) {
      this.dialogFormVisible = false;
      this.$refs["ruleForm"].resetFields();
      done();
      return false;
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
      if (!!this.timeChange) {
        this.paramsdict["timeinfo"] = JSON.stringify(this.timeChange);
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
        .dispatch("displaystand/GetDisplaystand", dataInfo)
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
    // ----------- 分页-----------
    // 全选
    selectAllData() {
      this.$refs.tableForm.toggleAllSelection();
    },
    // 全删
    delAllData() {
      const temp = this.$refs.tableForm.selection;
      const h = this.$createElement;
      if (temp.length === 0) {
        this.$notify({
          message: h("b", { style: "color: red" }, "请先选择行，才能删除"),
          duration: 2000,
        });
        return false;
      }
      let arr1 = [];

      for (let t in temp) {
        arr1.push({ id: temp[t].id, onlyid: temp[t].onlyid });
        this.pagin.total -= 1;
      }
      this.$store
        .dispatch(
          "displaystand/DelDisplaystand",
          JSON.stringify({ data: arr1 })
        )
        .then((response) => {
          this.getAllInfo();
          const { code, msg } = response;
          this.$message({
            type: code.toString().substr(0, 1) === "2" ? "success" : "error",
            message: msg,
          });
        });
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
  color: #260fe0;
}
.amountStyle >>> .el-form-item__label,
.amountStyle >>> .el-input__inner {
  color: #260fe0;
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