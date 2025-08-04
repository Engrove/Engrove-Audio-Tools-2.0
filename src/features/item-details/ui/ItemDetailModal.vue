<!-- src/features/item-details/ui/ItemDetailModal.vue -->
<template>
  <BaseModal :show="show" @close="emit('close')" :max-width="'max-w-4xl'">
    <div class="item-detail-modal" v-if="item">
      <!-- ============================================= -->
      <!-- Header Zone -->
      <!-- ============================================= -->
      <header class="item-detail-modal__header">
        <div class="header-main">
          <h1 class="header-main__model">{{ item.manufacturer }} {{ item.model }}</h1>
          <p class="header-main__source">Source: {{ item.source_name }}</p>
        </div>
        <div class="header-tag" :class="`tag--${item.type.toLowerCase()}`">
          {{ item.type }}
        </div>
      </header>

      <!-- ============================================= -->
      <!-- Core Data & Synergy Zone Wrapper -->
      <!-- ============================================= -->
      <div class="item-detail-modal__body-wrapper">
        <!-- ============================================= -->
        <!-- Core Data Zone -->
        <!-- ============================================= -->
        <main class="item-detail-modal__content">
          <div
            v-for="group in groupedData"
            :key="group.title"
            class="spec-group"
          >
            <h2 class="spec-group__title">{{ group.title }}</h2>
            <dl class="spec-group__list">
              <div
                v-for="spec in group.items"
                :key="spec.key"
                class="spec-item"
              >
                <dt class="spec-item__label">{{ spec.label }}</dt>
                <dd class="spec-item__value">
                  {{ spec.value }}
                  <span v-if="spec.unit" class="spec-item__unit">{{ spec.unit }}</span>
                </dd>
              </div>
            </dl>
          </div>
        </main>

        <!-- ============================================= -->
        <!-- Synergy Zone -->
        <!-- ============================================= -->
        <aside class="item-detail-modal__synergy">
          <div class="synergy-panel">
            <h2 class="synergy-panel__title">Synergy Analysis</h2>
            <div class="synergy-panel__content">
              <p class="synergy-panel__placeholder-text">
                AI-driven analysis and sonic signature prediction are coming soon. This feature will provide insights into the component's compatibility and potential sound characteristics.
              </p>
            </div>
          </div>
        </aside>
      </div>

    </div>
  </BaseModal>
</template>

<script setup>
// =============================================
// File history
// =============================================
// 2025-08-04: Created by Frankensteen.
//             - Complete rewrite based on approved plan for Steg 23.
//             - Implements a "multi-zon" view (Header, Core Data, Synergy).
//             - Uses a computed property `groupedData` to transform flat item data into a structured, curated view.
//             - Handles missing data gracefully to support different item types (cartridges, tonearms).
//             - Fully responsive and styled according to Global UI-Standard.
//

// =============================================
// Instruktioner vid skapande av fil
// =============================================
// Kärndirektiv: Fullständig kod, alltid. Inga genvägar.
// Principen "Explicit Alltid": All logik ska vara tydlig och fullständig.
// API-kontraktsverifiering: Props och emits utgör ett tydligt kontrakt.
// Red Team Alter Ego-granskning: Felresiliens (v-if="item", datafiltrering), Interaktionsrisker (enkel emit), Semantik och Läsbarhet (grupperad data, BEM-liknande klasser).
// Obligatorisk Refaktorisering: Logiken för datatransformation är centraliserad i `groupedData`.
//

import { computed } from 'vue';
import BaseModal from '@/shared/ui/BaseModal.vue';

// =============================================
// Component Interface (Props & Emits)
// =============================================
const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  item: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(['close']);

// =============================================
// Data Transformation Logic
// =============================================
// This computed property transforms the flat `item` object into a structured
// array of groups for rendering. It also filters out any properties that
// are not present in the current item, making it adaptable for both
// cartridges and tonearms.
const groupedData = computed(() => {
  if (!props.item) {
    return [];
  }

  // A definitive, curated list of all potential specs, organized into logical groups.
  const specMap = [
    {
      title: 'Physical Properties',
      items: [
        { key: 'weight_g', label: 'Weight', unit: 'g' },
        { key: 'effective_mass_g', label: 'Effective Mass', unit: 'g' },
        { key: 'effective_length_mm', label: 'Effective Length', unit: 'mm' },
        { key: 'mounting_to_stylus_mm', label: 'Mounting to Stylus', unit: 'mm' },
        { key: 'overhang_mm', label: 'Overhang', unit: 'mm' },
        { key: 'offset_angle_deg', label: 'Offset Angle', unit: '°' },
      ],
    },
    {
      title: 'Stylus & Compliance',
      items: [
        { key: 'stylus_type', label: 'Stylus Type', unit: null },
        { key: 'tracking_force_g', label: 'Tracking Force', unit: 'g' },
        { key: 'compliance_dynamic_10hz', label: 'Dynamic Compliance (10Hz)', unit: 'µm/mN' },
        { key: 'compliance_static_cu', label: 'Static Compliance', unit: 'CU' },
      ],
    },
    {
      title: 'Electrical Properties',
      items: [
        { key: 'output_voltage_mv', label: 'Output Voltage', unit: 'mV' },
        { key: 'internal_impedance_ohms', label: 'Internal Impedance', unit: 'Ω' },
        { key: 'recommended_load_ohms', label: 'Recommended Load', unit: 'Ω' },
        { key: 'capacitance_pf', label: 'Recommended Capacitance', unit: 'pF' },
        { key: 'dc_resistance_ohms', label: 'DC Resistance', unit: 'Ω' },
        { key: 'inductance_mh', label: 'Inductance', unit: 'mH' },
      ],
    },
     {
      title: 'Classification',
      items: [
        { key: 'tags', label: 'Tags', unit: null },
        { key: 'notes', label: 'Notes', unit: null },
      ]
    }
  ];

  // Process the map to build the final array for the template.
  return specMap
    .map(group => {
      const populatedItems = group.items
        .map(spec => ({
          ...spec,
          value: props.item[spec.key],
        }))
        .filter(spec => spec.value !== undefined && spec.value !== null && spec.value !== '' && (!Array.isArray(spec.value) || spec.value.length > 0));

      return {
        ...group,
        items: populatedItems,
      };
    })
    .filter(group => group.items.length > 0);
});

</script>

<style scoped>
.item-detail-modal {
  padding: var(--spacing-6);
  color: var(--text-medium-emphasis);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

/* Header */
.item-detail-modal__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-4);
  border-bottom: 1px solid var(--border-primary);
  padding-bottom: var(--spacing-4);
}

.header-main__model {
  color: var(--text-high-emphasis);
  font-size: var(--font-size-h2);
  font-weight: var(--font-weight-bold);
  line-height: 1.2;
}

.header-main__source {
  font-size: var(--font-size-small);
  color: var(--text-low-emphasis);
  margin-top: var(--spacing-1);
}

.header-tag {
  flex-shrink: 0;
  padding: var(--spacing-1) var(--spacing-3);
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-medium);
  text-transform: uppercase;
  background-color: var(--surface-tertiary);
  color: var(--text-medium-emphasis);
}

.header-tag.tag--mm, .header-tag.tag--mc {
    background-color: hsl(210, 100%, 30%);
    color: hsl(210, 100%, 95%);
}
.header-tag.tag--tonearm {
    background-color: hsl(180, 100%, 30%);
    color: hsl(180, 100%, 95%);
}


/* Body Wrapper */
.item-detail-modal__body-wrapper {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-8);
}

/* Main Content */
.item-detail-modal__content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

.spec-group__title {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-semibold);
  color: var(--text-high-emphasis);
  margin-bottom: var(--spacing-4);
  padding-bottom: var(--spacing-2);
  border-bottom: 1px solid var(--border-primary);
}

.spec-group__list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-4);
}

.spec-item {
  display: flex;
  flex-direction: column;
}

.spec-item__label {
  font-size: var(--font-size-small);
  color: var(--text-low-emphasis);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.spec-item__value {
  font-family: var(--font-family-data);
  font-size: var(--font-size-data);
  color: var(--text-medium-emphasis);
  margin-top: var(--spacing-1);
}

.spec-item__unit {
  font-family: var(--font-family-body);
  font-size: var(--font-size-small);
  color: var(--text-low-emphasis);
  margin-left: var(--spacing-1);
}

/* Synergy Panel */
.item-detail-modal__synergy {
  padding-left: var(--spacing-8);
  border-left: 1px solid var(--border-primary);
}

.synergy-panel__title {
  font-size: var(--font-size-h3);
  font-weight: var(--font-weight-semibold);
  color: var(--text-high-emphasis);
  margin-bottom: var(--spacing-4);
}

.synergy-panel__content {
  background-color: var(--surface-tertiary);
  border-radius: var(--border-radius-medium);
  padding: var(--spacing-4);
}

.synergy-panel__placeholder-text {
  font-size: var(--font-size-body);
  color: var(--text-medium-emphasis);
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 900px) {
  .item-detail-modal__body-wrapper {
    grid-template-columns: 1fr;
    gap: var(--spacing-6);
  }

  .item-detail-modal__synergy {
    padding-left: 0;
    border-left: none;
    border-top: 1px solid var(--border-primary);
    padding-top: var(--spacing-6);
  }
}

@media (max-width: 640px) {
  .item-detail-modal {
    padding: var(--spacing-4);
  }
  
  .item-detail-modal__header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-main__model {
    font-size: var(--font-size-h3);
  }

  .spec-group__list {
    grid-template-columns: 1fr;
  }
}
</style>
<!-- src/features/item-details/ui/ItemDetailModal.vue -->
