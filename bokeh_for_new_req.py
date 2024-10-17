import pandas as pd
from datetime import datetime
pd.options.mode.copy_on_write = True
from bokeh.io import output_file, reset_output, show
from bokeh.layouts import gridplot, layout, column, row
from bokeh.models import Div, Styles, Tabs, TabPanel
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.models import Button, CustomJS, Checkbox, CustomJSFilter, CDSView, Select, AutocompleteInput
from bokeh.models import NumeralTickFormatter, NumberFormatter, HTMLTemplateFormatter

# Configure header text
HomeHeaderText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h1>Claims Check<h1>
</div>
"""
# Configure displaying of total records
HomeMetricTotalRecordsText = """
<div style="color: #ffffff; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <p>Total Records</p><h2><b>{TotalRecords}</b></h2>
</div>
"""
# Configure displaying of unique contract
HomeMetricUniqueContractsText = """
<div style="color: #ffffff; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <p>Unique Contracts</p><h2><b>{UniqueContracts}</b></h2>
</div>
"""
# Configure displaying of unique supplier
HomeMetricUniqueSuppliersText = """
<div style="color: #ffffff; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <p>Unique Suppliers</p><h2><b>{UniqueSuppliers}</b></h2>
</div>
"""
# Configure displaying of unique sites
HomeMetricUniqueSitesText = """
<div style="color: #ffffff; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <p>Unique Sites</p><h2><b>{UniqueSites}</b></h2>
</div>
"""
# Configure displaying of header text for claims by year section
ClaimsByYearHeaderText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h2>Checks on Freight Pay Data</h2>
</div>
"""
# Configure displaying of footer text for claims by year section
ClaimsByYearFooterText = """
<div style="color:#4d4f5c; text-align:left; margin:0; position: absolute;">
    <p><b>Data Sources:</b> SupplierVouchers Data</p>
    <p><b>Miscellaneous Vouchers:</b> Downloadable Data for Miscellaneous Vouchers</p>
    </div>
"""
# Configure displaying of header text for supplier vouchers section
SupplierVouchersHeaderText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h2>Supplier Vouchers</h2>
</div>
"""
# Configure displaying of header text for tender reject section
TenderRejectedHeaderText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h2>Tender Rejected</h2>
</div>
"""
# Configure displaying of header text for canceled payment section
CanceledPaymentsHeaderText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h2>Pay Cancellation</h2>
</div>
"""
# Configure displaying of header text for zero charge section
ZeroChargePaymentsHeaderText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h2>Zero Charge</h2>
</div>
"""
# Configure displaying of header text for missing supply section
MissingSupplyPaymentsHeaderText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h2>Missing Supplier Vouchers</h2>
</div>
"""
# Configure displaying of header text for late payment section
MissingPaymentsHeaderText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h2>Miscellaneous Vouchers</h2>
</div>
"""

# Configure displaying of header text for late supplier percentages section
MissingPercentageText = """
<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);">
    <h2>Missing Supplier Percentages</h2>
</div>
"""
#####################
##### CSS Styles ####
#####################

# Styles for headers
HeaderStyles = {
    "margin": "0",
    "color": "#428BCA",
    "text-align": "center"
}

# Styles for horizontal line breaks
HorizontalBreakStyles = {
    "margin": "0",
    "background": "#43cea2",
    "background": "-webkit-linear-gradient(to left, #185a9d, #43cea2)",
    "background": "linear-gradient(to right, #185a9d, #43cea2)"
}

# Styles for horizontal divs
HorizontalDivStyles = Styles(
    margin="0"
)

# Styles for vertical divs
VerticalDivStyles = Styles(
    margin="0"
)

# Styles for metric-related divs
MetricDivStyles = Styles(
    transform="perspective(75em) rotateX(0deg)",
    margin="0px",
    # background_color="#f5f5f5",
    background_color="#0d6efd",
    opacity=".8",
    box_shadow="rgba(22, 31, 39, 0.42) 0px 60px 123px -25px, rgba(19, 26, 32, 0.08) 0px 35px 75px -35px",
    border_radius="10px",
    border="1px solid",
    border_color="rgb(213, 220, 226) rgb(213, 220, 226) rgb(184, 194, 204)"
)

# Javascript for exporting data
ExportDataJavaScript = """
function getcsv(source) {
    const columns = Object.keys(source.data)
    const nrows = source.get_length()
    const lines = [columns.join(',')];  // Use comma as delimiter for column headers

    for (let i = 0; i < nrows; i++) {
        let row = [];
        for (let j = 0; j < columns.length; j++) {
            const column = columns[j];
            // Encapsulate each field in double quotes and escape existing quotes
            const value = source.data[column][i].toString().replace(/"/g, '""');
            row.push('"' + value + '"');
        }
        lines.push(row.join(','));  // Comma as delimiter for data
    }
    return lines.join('\\n').concat('\\n');
}

var filetext = getcsv(source);
const blob = new Blob([filetext], {type: 'text/csv; charset=utf-8;'});

// Addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, file);
} else {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = file;
    link.target = '_blank';
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'));
}
"""
########################################################################################################################################################

##################################################
# TAB 0: Miscellaneous Summary
##################################################

# Path to the new output file
output_file_path = 'output/dashboard_helper_new_req.xlsx'

# Load the new output file
ClaimsByYearDf = pd.read_excel(output_file_path)

# Display the data for verification
print(ClaimsByYearDf)

# Convert data types
ClaimsByYearDf = ClaimsByYearDf.convert_dtypes(convert_string=True)

# Configure data source
ClaimsByYearSource = ColumnDataSource(ClaimsByYearDf)

# Configure table columns
ClaimsByYearColumns = [
    TableColumn(field="Month", title="Month", width=150),
    TableColumn(field="Total Records", title="Total Records", width=150, formatter=NumberFormatter(format="0,0"))
]

# Configure table
ClaimsByYearTable = DataTable(
    source=ClaimsByYearSource,
    columns=ClaimsByYearColumns,
    index_position=None,
    reorderable=False,
    width=1500,
    height=400,
    height_policy='auto'
)

# Configure gridplot
ClaimsByYearGridPlot = gridplot(
    children=[
        [Div(styles={"margin": "0"}, height=10, width=10), Div(styles={"margin": "0"}, height=10, width=1500)],
        [Div(styles={"margin": "0"}, height=2, width=10), Div(styles={"margin": "0", "background": "#43cea2", "background": "-webkit-linear-gradient(to left, #185a9d, #43cea2)", "background": "linear-gradient(to right, #185a9d, #43cea2)"}, height=2, width=1500)],
        [Div(styles={"margin": "0"}, height=50, width=10), Div(text="""<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);"><h2>Summary of Miscellaneous Vouchers</h2></div>""", height=50, width=1500)],
        [Div(styles={"margin": "0"}, height=10, width=10), ClaimsByYearTable],
        [Div(styles={"margin": "0"}, height=50, width=10), Div(text=ClaimsByYearFooterText, height=50, width=1500)]
    ],
    toolbar_location=None
)

########################################################################################################################################################

##################################################
# TAB 1: Miscellaneous Vouchers
##################################################

# Read the data
PayReconciliationMissingPaymentDf = pd.read_excel('output/MiscFilteredAllMonths.xlsx')
PayReconciliationMissingPaymentDf.fillna("", inplace=True)
print("Freight Auction Pay Reconciliation Missing Payment Vouchers Record Count: " + str(PayReconciliationMissingPaymentDf.shape))

# Configure source
PayReconciliationMissingPaymentSource = ColumnDataSource(PayReconciliationMissingPaymentDf)

# Create AutocompleteInput for 'CONTRACT' field
PayReconciliationMissingPaymentContractCompletions = [str(contract) for contract in PayReconciliationMissingPaymentDf['CONTRACT'].unique()]
PayReconciliationMissingPaymentContractCompletions.sort()

# AutocompleteInput for CONTRACT
PayReconciliationMissingPaymentContractAutocompleteInput = AutocompleteInput(
    title="Search Contract",
    search_strategy="includes",
    case_sensitive=False,
    restrict=False,
    placeholder='',
    completions=PayReconciliationMissingPaymentContractCompletions,
    width=200
)

# Initial Dropdown for SUPPLIER, MONTH, and VOUCHER REFERENCE (these will get updated dynamically)
PayReconciliationMissingPaymentSupplierSelect = Select(
    title="Supplier",
    value='All',
    options=['All']
)

PayReconciliationMissingPaymentMonthSelect = Select(
    title="Month",
    value='All',
    options=['All']
)

PayReconciliationMissingPaymentVoucherReferenceSelect = Select(
    title="Voucher Reference",
    value='All',
    options=['All']
)

# CONTRACT autocomplete callback
PayReconciliationMissingPaymentContractCallback = CustomJS(
    args=dict(source=PayReconciliationMissingPaymentSource, contract_autocomplete=PayReconciliationMissingPaymentContractAutocompleteInput,
              supplier_select=PayReconciliationMissingPaymentSupplierSelect, month_select=PayReconciliationMissingPaymentMonthSelect,
              voucher_reference_select=PayReconciliationMissingPaymentVoucherReferenceSelect),
    code="""
    const contract = contract_autocomplete.value.toLowerCase();
    const indices = [];
    const suppliers = new Set();
    const months = new Set();
    const voucherReferences = new Set();

    // Loop over all data to filter contracts and collect relevant suppliers, months, and voucher references
    for (let i = 0; i < source.get_length(); i++) {
        const contract_value = source.data['CONTRACT'][i].toString().toLowerCase();
        if (contract === '' || contract_value.includes(contract)) {  // Supposed to allow partial matching but not working
            indices.push(i);
            suppliers.add(source.data['SUPPLIER'][i].toString());
            months.add(source.data['Month'][i].toString());
            voucherReferences.add(source.data['VOUCHER REFERENCE'][i].toString());
        }
    }

    // Update dropdowns based on filtered contracts
    supplier_select.options = ['All'].concat(Array.from(suppliers));
    supplier_select.value = 'All';
    
    month_select.options = ['All'].concat(Array.from(months));
    month_select.value = 'All';
    
    voucher_reference_select.options = ['All'].concat(Array.from(voucherReferences));
    voucher_reference_select.value = 'All';

    // Update the data table based on contract filtering
    source.selected.indices = indices;
    source.change.emit();
    """
)
PayReconciliationMissingPaymentContractAutocompleteInput.js_on_change('value', PayReconciliationMissingPaymentContractCallback)

# Supplier select callback to dynamically update the month and voucher reference based on supplier
PayReconciliationMissingPaymentSupplierCallback = CustomJS(
    args=dict(
        source=PayReconciliationMissingPaymentSource,
        supplier_select=PayReconciliationMissingPaymentSupplierSelect,
        month_select=PayReconciliationMissingPaymentMonthSelect,
        contract_autocomplete=PayReconciliationMissingPaymentContractAutocompleteInput,
        voucher_reference_select=PayReconciliationMissingPaymentVoucherReferenceSelect
    ),
    code="""
    const supplier = supplier_select.value;
    const indices = [];
    const months = new Set();
    const voucherReferences = new Set();

    // Filter data by supplier and collect relevant months and voucher references
    for (let i = 0; i < source.get_length(); i++) {
        if (supplier === 'All' || source.data['SUPPLIER'][i] === supplier) {
            indices.push(i);
            months.add(source.data['Month'][i].toString());
            voucherReferences.add(source.data['VOUCHER REFERENCE'][i].toString());
        }
    }

    // Update dropdowns based on supplier filtering
    month_select.options = ['All'].concat(Array.from(months));
    month_select.value = 'All';
    
    voucher_reference_select.options = ['All'].concat(Array.from(voucherReferences));
    voucher_reference_select.value = 'All';

    source.selected.indices = indices;
    source.change.emit();
    """
)
PayReconciliationMissingPaymentSupplierSelect.js_on_change('value', PayReconciliationMissingPaymentSupplierCallback)

# Month select callback to dynamically update the supplier and voucher reference based on the month
PayReconciliationMissingPaymentMonthCallback = CustomJS(
    args=dict(
        source=PayReconciliationMissingPaymentSource,
        supplier_select=PayReconciliationMissingPaymentSupplierSelect,
        month_select=PayReconciliationMissingPaymentMonthSelect,
        contract_autocomplete=PayReconciliationMissingPaymentContractAutocompleteInput,
        voucher_reference_select=PayReconciliationMissingPaymentVoucherReferenceSelect
    ),
    code="""
    const month = month_select.value;
    const indices = [];
    const suppliers = new Set();
    const voucherReferences = new Set();

    // Filter data by month and collect relevant suppliers and voucher references
    for (let i = 0; i < source.get_length(); i++) {
        if (month === 'All' || source.data['Month'][i] === month) {
            indices.push(i);
            suppliers.add(source.data['SUPPLIER'][i].toString());
            voucherReferences.add(source.data['VOUCHER REFERENCE'][i].toString());
        }
    }

    // Update dropdowns based on month filtering
    supplier_select.options = ['All'].concat(Array.from(suppliers));
    supplier_select.value = 'All';
    
    voucher_reference_select.options = ['All'].concat(Array.from(voucherReferences));
    voucher_reference_select.value = 'All';

    source.selected.indices = indices;
    source.change.emit();
    """
)
PayReconciliationMissingPaymentMonthSelect.js_on_change('value', PayReconciliationMissingPaymentMonthCallback)

# VOUCHER REFERENCE select callback to filter based on voucher reference
PayReconciliationMissingPaymentVoucherReferenceCallback = CustomJS(
    args=dict(source=PayReconciliationMissingPaymentSource, voucher_reference_select=PayReconciliationMissingPaymentVoucherReferenceSelect),
    code="""
    const voucher_reference = voucher_reference_select.value;
    const indices = [];
    for (let i = 0; i < source.get_length(); i++) {
        if (voucher_reference === 'All' || source.data['VOUCHER REFERENCE'][i].toString() === voucher_reference) {
            indices.push(i);
        }
    }
    source.selected.indices = indices; // Update selected indices
    source.change.emit();
    """
)
PayReconciliationMissingPaymentVoucherReferenceSelect.js_on_change('value', PayReconciliationMissingPaymentVoucherReferenceCallback)

# Checkbox to filter out empty 'PAYMENT DATE'
checkbox_filter_paid = Checkbox(label="Paid Only", active=False)

# Checkbox to show only rows where 'PAYMENT DATE' is empty
checkbox_filter_unpaid = Checkbox(label="Unpaid Only", active=False)

# Filter based on supplier, month, contract, voucher reference, and checkbox selection
PayReconciliationMissingPaymentFilter = CustomJSFilter(
    args=dict(
        supplier_select=PayReconciliationMissingPaymentSupplierSelect,
        month_select=PayReconciliationMissingPaymentMonthSelect,
        contract_autocomplete=PayReconciliationMissingPaymentContractAutocompleteInput,
        voucher_reference_select=PayReconciliationMissingPaymentVoucherReferenceSelect,
        checkbox_paid=checkbox_filter_paid,
        checkbox_unpaid=checkbox_filter_unpaid
    ),
    code="""
    const indices = [];
    const selectedSupplier = supplier_select.value;
    const selectedMonth = month_select.value;
    const contract = contract_autocomplete.value;
    const voucher_reference = voucher_reference_select.value;
    const only_show_paid = checkbox_paid.active;
    const unpaid_only = checkbox_unpaid.active;

    for (let i = 0; i < source.get_length(); i++) {
        const supplierPaymentDate = source.data['PAYMENT DATE'][i];

        if ((selectedSupplier === 'All' || source.data['SUPPLIER'][i] === selectedSupplier) &&
            (selectedMonth === 'All' || source.data['Month'][i] === selectedMonth) &&
            (contract === '' || source.data['CONTRACT'][i].toString().includes(contract)) &&
            (voucher_reference === 'All' || source.data['VOUCHER REFERENCE'][i].toString() === voucher_reference) &&
            (!only_show_paid || supplierPaymentDate !== '') &&
            (!unpaid_only || supplierPaymentDate === '')) {
            indices.push(i);
        }
    }
    return indices;
    """
)

# Add checkbox change callback to refresh the data source
checkbox_callback = CustomJS(
    args=dict(source=PayReconciliationMissingPaymentSource),
    code="""
    source.change.emit();
    """
)
checkbox_filter_paid.js_on_change('active', checkbox_callback)
checkbox_filter_unpaid.js_on_change('active', checkbox_callback)

# Configure CDS view
PayReconciliationMissingPaymentView = CDSView(filter=PayReconciliationMissingPaymentFilter)

# Configure table columns
PayReconciliationMissingPaymentColumns = [
    TableColumn(field='SUPPLIER', title='Supplier'),
    TableColumn(field='CONTRACT', title='Contract', width=100),
    TableColumn(field='CHECK NUMBER', title='Check Number'),
    TableColumn(field='VOUCHER CREATED', title='Voucher Created'),
    TableColumn(field='PAYMENT DATE', title='Payment Date'),
    TableColumn(field='VOUCHER REFERENCE', title='Voucher Reference', width=500),
    TableColumn(field='BILLED AMT', title='Billed Amount', formatter=NumberFormatter(format='$ 0,0.00')),
    TableColumn(field='PAYMENT AMT', title='Payment Amount', formatter=NumberFormatter(format='$ 0,0.00'))
]

# Configure table
PayReconciliationMissingPaymentTable = DataTable(
    source=PayReconciliationMissingPaymentSource,
    columns=PayReconciliationMissingPaymentColumns,
    view=PayReconciliationMissingPaymentView,
    index_position=None,
    reorderable=False,
    width=1500,
    height=500,
    height_policy='auto'
)

# Configure download button
PayReconciliationMissingPaymentDownloadButton = Button(label="Download", button_type="primary", width=50)
PayReconciliationMissingPaymentDownloadButton.js_on_click(CustomJS(
    args=dict(file='MiscellaneousVouchersData.csv', source=PayReconciliationMissingPaymentSource),
    code="""
    function getcsv(source) {
        const columns = Object.keys(source.data)
        const nrows = source.get_length()
        const lines = [columns.join(',')];  // Use comma as delimiter for column headers

        for (let i = 0; i < nrows; i++) {
            let row = [];
            for (let j = 0; j < columns.length; j++) {
                const column = columns[j];
                const value = source.data[column][i].toString().replace(/"/g, '""');
                row.push('"' + value + '"');
            }
            lines.push(row.join(','));
        }
        return lines.join('\\n').concat('\\n');
    }

    var filetext = getcsv(source);
    const blob = new Blob([filetext], {type: 'text/csv; charset=utf-8;'});

    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, file);
    } else {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = file;
        link.target = '_blank';
        link.style.visibility = 'hidden';
        link.dispatchEvent(new MouseEvent('click'));
    }
    """
))

# Configure gridplot
PayReconciliationMissingPaymentGridPlot = gridplot(
    children=[
        [Div(styles={"margin": "0"}, height=10, width=10), Div(styles={"margin": "0"}, height=10, width=1500)],
        [Div(styles={"margin": "0"}, height=2, width=10), Div(styles={"margin": "0", "background": "#43cea2", "background": "-webkit-linear-gradient(to left, #185a9d, #43cea2)", "background": "linear-gradient(to right, #185a9d, #43cea2)"}, height=2, width=1500)],
        [Div(styles={"margin": "0"}, height=50, width=10), Div(text="""<div style="color:#4d4f5c; text-align:center; margin:0; position: absolute; top: 50%; left: 50%; -ms-transform: translate(-50%, -50%); transform: translate(-50%, -50%);"><h2>Miscellaneous Vouchers</h2></div>""", height=50, width=1500)],
        [Div(styles={"margin": "0"}, height=50, width=10), row(PayReconciliationMissingPaymentContractAutocompleteInput, PayReconciliationMissingPaymentSupplierSelect, PayReconciliationMissingPaymentMonthSelect, PayReconciliationMissingPaymentVoucherReferenceSelect)],
        [Div(styles={"margin": "0"}, height=10, width=10), row(checkbox_filter_paid, checkbox_filter_unpaid)],
        [Div(styles={"margin": "0"}, height=10, width=10), PayReconciliationMissingPaymentTable],
        [Div(styles={"margin": "0"}, height=10, width=10), PayReconciliationMissingPaymentDownloadButton],
        [Div(styles={"margin": "0"}, height=2, width=10), Div(styles={"margin": "0", "background": "#43cea2", "background": "-webkit-linear-gradient(to left, #185a9d, #43cea2)", "background": "linear-gradient(to right, #185a9d, #43cea2)"}, height=2, width=1500)]
    ],
    toolbar_location=None
)

########################################################################################################################################################

# Configure tabs
tabs = []
tabs.append(TabPanel(child=ClaimsByYearGridPlot, title="Miscellaneous Summary"))
tabs.append(TabPanel(child=PayReconciliationMissingPaymentGridPlot, title="Miscellaneous Vouchers"))

# Create report
reset_output()
output_file('Output/Miscellaneous Dashboard.html', mode='cdn', title='Miscellaneous Dashboard')
show(Tabs(tabs=tabs))
