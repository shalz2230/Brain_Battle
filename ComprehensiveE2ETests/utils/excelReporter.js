const ExcelJS = require('exceljs');
const path = require('path');
const fs = require('fs');

async function generateExcelReport(testResults) {
    const workbook = new ExcelJS.Workbook();
    workbook.creator = 'Selenium E2E Suite';
    workbook.created = new Date();

    const sheet = workbook.addWorksheet('Test Results');
    
    sheet.columns = [
        { header: 'Test Suite', key: 'suite', width: 30 },
        { header: 'Test Name', key: 'name', width: 50 },
        { header: 'Status', key: 'status', width: 15 },
        { header: 'Duration (ms)', key: 'duration', width: 15 },
        { header: 'Error Message', key: 'error', width: 50 }
    ];

    sheet.getRow(1).font = { bold: true };
    sheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FFD3D3D3' }
    };

    testResults.forEach(result => {
        const row = sheet.addRow(result);
        
        // Color code status
        if (result.status === 'Pass') {
            row.getCell('status').font = { color: { argb: 'FF008000' } };
        } else if (result.status === 'Fail') {
            row.getCell('status').font = { color: { argb: 'FFFF0000' } };
        }
    });

    const reportsDir = path.join(__dirname, '..', 'reports');
    if (!fs.existsSync(reportsDir)) {
        fs.mkdirSync(reportsDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filePath = path.join(reportsDir, `Comprehensive_E2E_Report_${timestamp}.xlsx`);

    await workbook.xlsx.writeFile(filePath);
    console.log(`Excel report saved to: ${filePath}`);
}

module.exports = { generateExcelReport };
