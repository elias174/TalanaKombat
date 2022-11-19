from game_engine import MovementCombo

MOVEMENTS_COMBO_J1 = {
    'DSDP': MovementCombo('DSD', 'P', 3, '{player_name} conecta un Taladoken'),
    'SDK': MovementCombo('SD', 'K', 2, '{player_name} conecta un Remuyuken')
}

MOVEMENTS_COMBO_J2 = {
    'SAK': MovementCombo('SA', 'K', 3, '{player_name} conecta un Remuyuken'),
    'ASAP': MovementCombo('ASA', 'P', 2, '{player_name} conecta un Taladoken')
}
