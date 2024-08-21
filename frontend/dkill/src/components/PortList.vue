<template>
  <div>
    <el-input v-model="search" placeholder="Search by port" @input="fetchPorts" style="width: 300px; margin-bottom: 10px;" />
    <el-table :data="ports" stripe style="width: 100%">
      <el-table-column prop="port" label="Port" width="180" />
      <el-table-column prop="pid" label="PID" width="180" />
      <el-table-column prop="state" label="State" width="180" />
      <el-table-column label="Actions">
        <template v-slot="scope">
          <el-button size="mini" type="danger" @click="killProcess(scope.row.pid)">Kill</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      :page-size.sync="perPage"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
      :current-page.sync="currentPage"
      :page-sizes="[5, 10, 20, 50]"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'

export default {
  name: 'PortList',
  setup() {
    const ports = ref([])
    const search = ref('')
    const total = ref(0)
    const currentPage = ref(1)
    const perPage = ref(10)

    const fetchPorts = async () => {
      try {
        const response = await axios.get('/api/ports', {
          params: {
            page: currentPage.value,
            per_page: perPage.value,
            search: search.value,
          },
        })
        ports.value = response.data.ports
        total.value = response.data.total
      } catch (error) {
        ElMessage.error('Failed to fetch ports.')
      }
    }

    const killProcess = async (pid) => {
      try {
        const response = await axios.post('/api/kill', { pid })
        if (response.data.status === 'success') {
          ElMessage.success(response.data.message)
          fetchPorts()
        } else {
          ElMessage.error(response.data.message)
        }
      } catch (error) {
        ElMessage.error('Failed to kill the process.')
      }
    }

    const handlePageChange = (page) => {
      currentPage.value = page
      fetchPorts()
    }

    const handleSizeChange = (size) => {
      perPage.value = size
      fetchPorts()
    }

    onMounted(() => {
      fetchPorts()
    })

    return {
      ports,
      search,
      total,
      currentPage,
      perPage,
      fetchPorts,
      killProcess,
      handlePageChange,
      handleSizeChange
    }
  }
}
</script>
