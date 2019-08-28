class SU2Config(object):

    def __init__(self, _default_path=None):
        self.yes_no_opts = {
            'YES': 'YES',
            'NO': 'NO',
        }
        # self._default_path = _default_path  # get it from come sort of cfg
        self._load_path = None
        self._save_path = None
        # self._user_provided_path = None
        self._use_default = False
        self.current_case = None

        self._physical_problem = 'EULER'
        self._units = 'SI'
        self._regime_type = 'INCOMPRESSIBLE'

        # COMPRESSIBLE FLOW PARAMS
        self._mach_number = 0.8
        self._aoa = 1.25
        self._sideslip = 0
        # initialization params
        self._init_option = 'REYNOLDS'
        # which value should be used for solution's
        # initialization
        self._freestream_option = 'TEMPERATURE_FS'
        self._freestream_pressure = 101325.0
        self._freestream_temperature = 288.15
        self._reynolds_number = 6.5e6
        self._reynolds_length = 1

        # INCOMPRESSIBLE FLOW PARAMS
        self._freestream_density = 1.2886
        # now defined as immutable
        # perhaps should be changed to list
        self._freestream_velociity = (1.0, 0.0, 0.0)
        self._freestream_viscosity = 1.853 * 0.00001

        # CL DRIVER DEFINITION
        self._fixed_cl_mode = 'NO'
        self._target_cl = 0.8
        self._dcl_alpha = 0.2
        self._update_alpha = 5
        self._iter_dcl_alpha = 500

        # REFERENCE VALUES DEF
        self._ref_origin_moment_x = 0.25
        self._ref_origin_moment_y = 0
        self._ref_origin_moment_z = 0
        self._ref_length = 1.0
        self._ref_area = 1.0
        self._ref_semi_span = 0

        # possible values
        # DIMENSIONAL, FREESTREAM_PRESS_EQ_ONE,
        # FREESTREAM_VEL_EQ_MACH, FREESTREAM_VEL_EQ_ONE
        self._ref_dimensionalization = 'DIMENSIONAL'
        self._ref_dimensionalization_opts = {
            'DIMENSIONAL': 'DIMENSIONAL',
            'FREESTREAM_PRESS_EQ_ONE': 'FREESTREAM_PRESS_EQ_ONE',
            'FREESTREAM_VEL_EQ_MACH': 'FREESTREAM_VEL_EQ_MACH',
            'FREESTREAM_VEL_EQ_ONE': 'FREESTREAM_VEL_EQ_ONE',
        }
        # possible values

        # IDEAL GAS, POLYTOPIC, VDV AND P-R CONSTANTSS
        # STANDARD_AIR, IDEAL_GAS, VW_GAS, PR_GAS
        self._fluid_model = 'STANDARD_AIR'
        self._fluid_model_opts = {
            'STANDARD_AIR': 'STANDARD_AIR',
            'IDEAL_GAS': 'IDEAL_GAS',
            'VW_GAS': 'VW_GAS',
            'PR_GAS': 'PR_GAS',
        }
        self._gamma_value = 1.4
        self._gas_constant = 287.058
        self._critical_temperature = 131.0
        self.critical_pressure = 3588550.0
        self._acentric_factor = 0.035

        # VISCOSITY MODEL
        self._viscosity_model = 'SUTHERLAND'
        self._viscosity_model_opts = {
            'SUTHERLAND': 'SUTHERLAND',
            'CONSTANT_VISCOSITY': 'CONSTANT_VISCOSITY',
        }

        # THERMAL CONDUCTIVITY MODEL
        # CONSTANT_CONDUCTIVITY, CONSTANT_PRANDTL
        self._conductivity_model = 'CONSTANT_PRANDTL'
        self._conductivity_model_opts = {
            'CONSTANT_CONDUCTIVITY': 'CONSTANT_CONDUCTIVITY',
            'CONSTANT_PRANDTL': 'CONSTANT_PRANDTL'
        }
        self._kt_constant = 0.0257

        # UNSTEADY SIMULATION
        # NO, TIME_STEPPING, DUAL_TIME_STEPPING-1_ST_ORDER,
        # DUAL_TIME_STEPPING-2_ND_ORDER, HARMONIC_BALANCE
        self._unsteady_simulation = 'NO'
        self._unsteady_simulation_opts = {
            'NO': 'NO',
            'TIME_STEPPING': 'TIME_STEPPING',
            'DUAL_TIME_STEPPING-1_ST_ORDER': 'DUAL_TIME_STEPPING-1_ST_ORDER',
            'DUAL_TIME_STEPPING-2_ND_ORDER': 'DUAL_TIME_STEPPING-2_ND_ORDER',
            'HARMONIC_BALANCE': 'HARMONIC_BALANCE'
        }
        self._unst_timestep = 0.0
        self._unst_time = 50.0
        self._unst_cfl_number = 0.0
        self._unst_init_iter = 200
        self._unst_restart_iter = 0

        # DYNAMIC MESH DEFINITION
        self._grid_movement = 'NO'
        self._grid_movement_opts = self.yes_no_opts

        self._grid_movement_kind = 'DEFORMING'
        # NONE, RIGID_MOTION, DEFORMING, ROTATING_FRAME,
        # MOVING_WALL, STEADY_TRANSLATION, FLUID_STRUCTURE,
        # AEROELASTIC, ELASTICITY, EXTERNAL,
        # AEROELASTIC_RIGID_MOTION, GUST
        self._grid_movement_kind_opts = {
            'NONE': 'NONE',
            'RIGID_MOTION': 'RIGID_MOTION',
            'DEFORMING': 'DEFORMING',
            'ROTATING_FRAME': 'ROTATING_FRAME',
            'MOVING_WALL': 'MOVING_WALL',
            'STEADY_TRANSLATION': 'STEADY_TRANSLATION',
            'FLUID_STRUCTURE': 'FLUID_STRUCTURE',
            'AEROELASTIC': 'AEROELASTIC',
            'ELASTICITY': 'ELASTICITY',
            'EXTERNAL': 'EXTERNAL',
            'AEROELASTIC_RIGID_MOTION': 'AEROELASTIC_RIGID_MOTION',
            'GUST': 'GUST'
        }

        self._mach_motion = 0.8
        self._marker_moving = ('NONE')

        self._motion_origin_x = 0.25
        self._motion_origin_y = 0.0
        self._motion_origin_z = 0.0

        # rad/s
        self._rotation_rate_x = 0.0
        self._rotation_rate_y = 0.0
        self._rotation_rate_z = 0.0

        # rad/s
        self._pitching_omega_x = 0.0
        self._pithcing_omega_y = 0.0
        self._pitching_omega_z = 0.0

        # deg
        self._pitching_ampl_x = 0.0
        self._pitching_ampl_y = 0.0
        self._pitching_ampl_z = 0.0

        # deg
        self._pitching_phase_x = 0.0
        self._pitching_phase_y = 0.0
        self._pitching_phase_z = 0.0

        # m/s
        self._translation_rate_x = 0.0
        self._translation_rate_y = 0.0
        self._translation_rate_z = 0.0

        # rad/s
        self._plunging_omega_x = 0.0
        self._plunging_omega_y = 0.0
        self._plunging_omega_z = 0.0

        self._move_motion_origin = 0
        self._move_motion_origin = {
            0: 0,
            1: 1
        }

        # AEROELASTIC SIMULATION
        # skipped for now - triggered by GRID_MOVEMENT_KIND

        # GUST SIMULATION
        self._gust_simulation = 'NO'
        self._gust_simulation_opts = self.yes_no_opts
        # rest of gust opts is skipped for now
        # gusts are disables by default

        # SUPERSONIC SIMULATION
        self._equiv_area = 'NO'
        self._equiv_area = self.yes_no_opts

        self._ea_int_limit = (1.6, 2.9, 1.0)
        self._ea_scale_factor = 1.0
        self._fix_aimuthat_line = 90.0
        self._drag_in_sonicboom = 0.0

        # ENGINE SIMULATION
        # skipped for now

        # INVERSE DESIGN SIMULATION
        self._inv_design_cp = 'NO'
        self._inv_design_cp_opts = self.yes_no_opts
        self._inv_design_heatflux = 'NO'
        self._inv_design_heatflux_opts = self.yes_no_opts

        # BODY FORCE DEF
        self._body_force = 'NO'
        self._body_force_opts = self.yes_no_opts
        self._body_force_vector = (0.0, 0.0, 0.0)

        # BOUNDARY CONDITIONS
        self._marker_euler = ('airfoil')
        self._marker_heatflux = ('NONE')
        self._marker_isothermal = ('NONE')
        self._marker_far = ('farfield')
        self._marker_sym = ('NONE')
        self._marker_internal = ('NONE')
        self._marker_nearfield = ('NONE')
        self._marker_interface = ('NONE')
        self._inlet_type = 'TOTAL_CONDITIONS'
        self._inlet_type_opts = {
            'TOTAL_CONDITIONS': 'TOTAL_CONDITIONS',
            'MASS_FLOW': 'MASS_FLOW'
        }
        self._inlet_type_opts_dict = {
            'TOTAL_CONDITIONS': (
                'inlet_marker', 'total_temp', 'total_pressure',
                'flow_direction_x', 'flow_direction_y', 'flow_direction_z'),
            # flow_direction is an unit vector
            'MASS_FLOW': (
                'inlet_marker', 'density', 'velocity_magnitude',
                'flow_direction_x', 'flow_direction_y', 'flow_direction_z'),
            # flow_direction is an unit vector
            'Incompressible': (
                'inlet_marker', 'NULL', 'velocity_magnitude',
                'flow_direction_x', 'flow_direction_y', 'flow_direction_z'),
            # flow_direction is an unit vector
        }
        self._marker_inlet = ('NONE')
        self._marker_outlet = ('NONE')
        # VARIABLES_JUMP, BC_THRUST,
        # % DRAG_MINUS_THRUST)
        self._actdisk_type = 'VARIABLES_JUMP'
        self._actdisk_type_opts = {
            'VARIABLES_JUMP': 'VARIABLES_JUMP',
            'BC_THRUST': 'BC_THRUST',
            'DRAG_MINUS_THRUST': 'DRAG_MINUS_THRUST',
        }
        self._actdisk_type_opts_dict = {
            'VARIABLES_JUMP': (
                'inlet face marker', 'outlet face marker',
                'Takeoff pressure jump (psf)', 'Takeoff temperature jump(R)',
                'Takeoff rev / min', 'Cruise pressure jump(psf)',
                'Cruise temperature jump(R)', 'Cruise rev / min'),
            'BC_THRUST': (
                'inlet face marker', 'outlet face marker',
                'Takeoff BC thrust (lbs)', 0.0, 'Takeoff rev / min',
                'Cruise BC thrust (lbs)', 0.0, 'Cruise rev/min'),
            'DRAG_MINUS_THRUST': (
                'inlet face marker', 'outlet face marker',
                'Takeoff Drag-Thrust (lbs)', 0.0, 'Takeoff rev / min',
                'Cruise Drag - Thrust(lbs)', 0.0, 'Cruise rev / min')
        }

        self._marker_actdisk = ('NONE')
        self._marker_supersonic_inlet = ('NONE')
        self._marker_supersonic_inlet_pattern = \
            ('inlet marker', 'temperature', 'static pressure',
             'velocity_x', 'velocity_y', 'velocity_z', '...')
        self._supersonic_outlet = ('NONE')

        self._marker_periodic = ('NONE')
        self._marker_periodic_pattern = \
            ('periodic marker', 'donor marker',
             'rotation_center_x', 'rotation_center_y',
             'rotation_center_z', 'rotation_angle_x-axis',
             'rotation_angle_y-axis', 'rotation_angle_z-axis',
             'translation_x', 'translation_y', 'translation_z',
             '...')

        self._engine_inflow_type = 'FAN_FACE_MACH'
        self._engine_inflow_type_opts = {
            'FAN_FACE_MACH': 'FAN_FACE_MACH',
            'FAN_FACE_PRESSURE': 'FAN_FACE_PRESSURE',
            'FAN_FACE_MDOT': 'FAN_FACE_MDOT'
        }

        self._marker_engine_inflow = ('NONE')
        self._marker_engine_inflow_pattern = \
            ('engine_inflow_marker', 'fan_face_mach', '...')

        self._marker_engine_exhaust = ('NONE')
        self._marker_engine_exhaust_pattern = \
            ('engine exhaust marker', 'total nozzle temp',
             'total nozzle pressure', '...')

        self._marker_normal_displ = ('NONE')
        self._marker_normal_displ_pattern = \
            ('displacement marker', 'displacement value normal to the surface',
             '...')
        self._marker_normal_load = ('NONE')
        self._marker_normal_load_pattern = \
            ('load marker', 'force value normal to the surface', '...')

        self._marker_pressure = ('NONE')
        self._marker_pressure_pattern = ('pressure_marker')

        self._marker_neumann = ('NONE')

        self._marker_dirichlet = ('NONE')

        self._marker_riemann = ('NONE')
        self._marker_riemann_pattern = \
            ('marker', 'data kind flag', 'list of data')

        self._marker_shroud = ('NONE')

        # Interface def - definition by providing zone names
        # which are connected by interfaces surfaces
        # eg. A and B share interface 1
        #     A and C share interface 2
        self._marker_zone_interface = ('NONE')
        self._marker_zone_interaface_pattern = \
            ('marker_A_on_interface_1',
             'marker_B_on_interface_1',
             'marker_A_on_interface_2',
             'marker_C_on_interface_2', '...')

        # same stuff here
        self._marker_fluid_interface = ('NONE')
        self._marker_fluid_interface_pattern = \
            ('marker_A_on_interface_1',
             'marker_B_on_interface_1',
             'marker_A_on_interface_2',
             'marker_C_on_interface_2', '...')

        # kind of interpolation between zones
        self._kind_interpolation = 'NEAREST_NEIGHBOR'
        self._kind_interpolation_opts = \
            ('NEAREST_NEIGHBOR', 'ISOPARAMETRIC', 'SLIDING_MESH')

        # INFLOW/OUTFLOW BOUNDARY CONDITIONS SPECIFIC FOR
        # TURBOMACHINERY
        # INFLOW (obilgtory | ..(opts).. | OUTFLOW (obligatory)
        self._marker_turbomachinery = \
            ('INFLOW', 'OUTMIX', 'INMIX', 'OUTFLOW')

        self._marker_mixingplane_interface = \
            ('OUTMIX', 'INMIX')
        # Giles boundary condition for inflow, outflow,
        # and mixing-plane
        self._marker_giles = ()
        self._marker_giles_inflow_pattern = \
            ('marker', 'TOTAL_CONDITIONS_PT', 'Total Pressure',
             'Total Temperature', 'Flow dir-norm', 'Flow dir-tang',
             'Flow dir-span', 'under-relax-avg', 'under-relax-fourier')

        self._marker_giles_outflow_pattern = \
            ('marker', 'STATIC_PRESSURE', 'Static Pressure value', '-', '-',
             '-', '-', 'under-relax-avg', 'under-relax-fourier')

        self._marker_giles_mixing_plane_pattern = \
            ('marker', 'MIXING_IN or MIXING_OUT', '-', '-', '-', '-', '-', '-',
             'under - relax - avg', 'under - relax - fourier')

        self._marker_giles_pattern = \
            (self._marker_giles_inflow_pattern,
             # as many times as you need
             self._marker_giles_mixing_plane_pattern,
             self._marker_giles_outflow_pattern)

        # full example of self._marker_giles_pattern
        # (INFLOW, TOTAL_CONDITIONS_PT, 413.6E+03, 477.6, 1.0, 0.0, 0.0, 1.0, 0.0,
        # OUTMIX, MIXING_OUT, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0,
        # INMIX, MIXING_IN, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.0,
        # OUTFLOW, STATIC_PRESSURE_1D, 67.46E+03, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        self._giles_extra_relaxfactor = (0.05, 0.05)
        self._spatial_fourier = 'NO'
        self._spatial_fourier_opts = self.yes_no_opts

        # TURBOMACHINERY SIMULATION

        # For each zone the kind ust be provided
        # A_kind B_kind ... LAST_kind
        self._turbomachinery_kind = \
            'CENTRIPETAL CENTRIPETAL_AXIAL'
        self._turbomachinery_kind_opts = {
            'AXIAL': 'AXIAL',
            'CENTRIPETAL': 'CENTRIPETAL',
            'CENTRIFUGAL': 'CENTRIFUGAL',
            'CENTRIPETAL_AXIAL': 'CENTRIPETAL_AXIAL',
            'AXIAL_CENTRIFUGAL': 'AXIAL_CENTRIFUGAL'
        }

        # apx across the interface
        self._mixingplane_interface_kind = 'LINEAR_INTERPOLATION'
        self._mixingplane_interface_kind_opts = \
            ('LINEAR_INTERPOLATION', 'NEAREST_SPAN', 'MATCHING')

        # specify turb. mixplane
        self._turbulent_mixingplane = 'NO'
        self._turbulent_mixingplane_opts = self.yes_no_opts

        # specify ramp option for outlet pressure
        self._ramp_outlet_pressure = 'NO'
        self._ramp_outlet_pressure_opts = self.yes_no_opts
        self._ramp_outlet_pressure_coeff = (400000.0, 10.0, 500)

        self._ramp_rotating_frame = 'NO'
        self._ramp_rotating_frame_opts = self.yes_no_opts

        self._ramp_rotating_frame_coeff = (0.0, 39.0, 500)
        self._average_process_kind = 'MIXEDOUT'
        self._average_process_kind_opts = \
            ('ALGEBRAIC', 'AREA', 'MASSSFLUX', 'MIXEDOUT')

        self._performance_average_process_kind = 'MIXEDOUT'
        self._performance_average_process_kind_opts = \
            ('ALGEBRAIC', 'AREA', 'MASSSFLUX', 'MIXEDOUT')

        self._mixedout_coeff = (1.0, 1.0e-05, 15)
        self._average_mach_limit = 0.05

        # SURFFACES IDENTIFICATION
        # Marker(s) of the surface in the surface flow solution file
        self._marker_plotting = ('airfoil')
        # Marker(s) of the surface where the non-dimensional
        # coefficients are evaluated.
        self._marker_monitoring = ('airfoil')
        # Viscous wall markers for which wall functions
        # must be applied. (NONE = no marker)
        self._marker_wall_functions = \
            ('airfoil', 'NO_WALL_FUNCTION')

        self._marker_wall_functions_pattern = \
            ('marker name', 'wall function type', '...')
        # Marker(s) of the surface where custom thermal BC's are defined.
        self._marker_python_custom = ('NONE')
        # Marker(s) of the surface where obj. func. (design problem) will be evaluated
        self._marker_designing = ('airfoil')
        # Marker(s) of the surface that is going to be analyzed in detail (massflow, average pressure, distortion, etc)
        self._marker_analyze = ('airfoil')
        # Method to compute the average value in MARKER_ANALYZE (AREA, MASSFLUX)
        self._marker_analyze_average = ('airfoil')
        self._marker_analyze_average_opts = \
            {'AREA': 'AREA',
             'MASSFLUX': 'MASSFLUX'
            }

        # COMMON PARAMETERS DEFINING THE NUMERICAL METHOD
        self._num_method_grad = 'GREEN_GAUSS'
        self._num_method_grad_opts = \
            {
                'GREEN_GAUSS': 'GREEN_GAUSS',
                'WEIGHTED_LEAST_SQUARES': 'WEIGHTED_LEAST_SQUARES'
            }
        # init val for Courant number
        self._cfl_number = 10.0
        self._cfl_adapt = 'NO'
        self._cfl_adapt_opts = self.yes_no_opts

        # (factor down, factor up, CFL min value, CFL max value)
        self._cfl_adapt_param = (1.5, 0.5, 1.25, 50.0)
        # Maximum Delta Time in local time stepping simulations
        self._max_delta_time = 1e6
        # Runge-Kutta alpha coefficients
        self._rk_alpha_coeff = (0.66667, 0.66667, 1.000000)
        self._objective_function = 'DRAG'
        self._objective_function_opts = \
        {
            'DRAG': 'DRAG',
            'LIFT': 'LIFT',
            'SIDEFORCE': 'SIDEFORCE',
            'MOMENT_X': 'MOMENT_X',
            'MOMENT_Y': 'MOMENT_Y',
            'MOMENT_Z': 'MOMENT_Z',
            'EFFICIENCY': 'EFFICIENCY',
            'EQUIVALENT_AREA': 'EQUIVALENT_AREA',
            'NEARFIELD_PRESSURE': 'NEARFIELD_PRESSURE',
            'FORCE_X': 'FORCE_X',
            'FORCE_Y': 'FORCE_Y',
            'FORCE_Z': 'FORCE_Z',
            'THRUST': 'THRUST',
            'TORQUE': 'TORQUE',
            'TOTAL_HEATFLUX': 'TOTAL_HEATFLUX',
            'MAXIMUM_HEATFLUX': 'MAXIMUM_HEATFLUX',
            'INVERSE_DESIGN_PRESSURE': 'INVERSE_DESIGN_PRESSURE',
            'INVERSE_DESIGN_HEATFLUX': 'INVERSE_DESIGN_HEATFLUX',
            'SURFACE_TOTAL_PRESSURE': 'SURFACE_TOTAL_PRESSURE',
            'SURFACE_MASSFLOW': 'SURFACE_MASSFLOW',
            'SURFACE_STATIC_PRESSURE': 'SURFACE_STATIC_PRESSURE',
            'SURFACE_MACH': 'SURFACE_MACH'
        }

        self._objective_wieght = 1.0

        # SLOPE LIMITER AND DISSIPATION SENSOR DEFINITION

        self._muscl_flow = 'YES'
        self._muscl_flow_opts = self.yes_no_opts

        self._slope_limiter_flow = 'VENKATAKRISHNAN'
        self._slope_limiter_flow_opts = \
            {
                'NONE': 'NONE',
                'VENKATAKRISHNAN': 'VENKATAKRISHNAN',
                'VENKATAKRISHNAN_WANG': 'VENKATAKRISHNAN_WANG',
                'BARTH_JESPERSEN': 'BARTH_JESPERSEN',
                'VAN_ALBADA_EDGE': 'VAN_ALBADA_EDGE'
            }
        self._muscl_turb = 'NO'
        self._muscl_turb_opts = self.yes_no_opts

        self._slope_limiter_turb = 'VENKATAKRISHNAN'
        self._slope_limiter_flow_opts = \
            {
                'NONE': 'NONE',
                'VENKATAKRISHNAN': 'VENKATAKRISHNAN',
                'VENKATAKRISHNAN_WANG': 'VENKATAKRISHNAN_WANG',
                'BARTH_JESPERSEN': 'BARTH_JESPERSEN',
                'VAN_ALBADA_EDGE': 'VAN_ALBADA_EDGE'
            }
        self._slope_limiter_adjflow = 'VENKATAKRISHNAN'
        self._slope_limiter_adjflow_opts = \
            {
                'NONE': 'NONE',
                'VENKATAKRISHNAN': 'VENKATAKRISHNAN',
                'VENKATAKRISHNAN_WANG': 'VENKATAKRISHNAN_WANG',
                'BARTH_JESPERSEN': 'BARTH_JESPERSEN',
                'VAN_ALBADA_EDGE': 'VAN_ALBADA_EDGE'
            }

        self._muscl_adjtrub = 'NO'
        self._muscl_adjtrub_opts = self.yes_no_opts

        self._slope_limiter_adjturb = 'VENKATAKRISHNAN'
        self._slope_limiter_adjturb_opts = \
            {
                'NONE': 'NONE',
                'VENKATAKRISHNAN': 'VENKATAKRISHNAN',
                'VENKATAKRISHNAN_WANG': 'VENKATAKRISHNAN_WANG',
                'BARTH_JESPERSEN': 'BARTH_JESPERSEN',
                'VAN_ALBADA_EDGE': 'VAN_ALBADA_EDGE'
            }

        self._venkat_limiter_coeff = 0.005
        self._adj_sharp_limiter_ceoff = 3.0
        self._limiter_iter = 999999
        # 1st order artificial dissipation coefficients for
        # the Lax–Friedrichs method ( 0.15 by default )
        self._lax_sensor_coeff = 0.15
        # 2nd and 4th order artificial dissipation coefficients for
        # the JST method ( 0.5, 0.02 by default )
        self._jst_sensor_coeff = (0.5, 0.02)
        # 1st order artificial dissipation coefficients for
        # the Lax–Friedrichs method ( 0.15 by default )
        self._adj_lax_sensor_coeff = 0.15
        # 2nd and 4th order artificial dissipation coefficients for
        # the JST method ( 0.5, 0.02 by default )
        self._adj_jst_sensor_coeff = (0.5, 0.05)

        # LINEAR SOLVER DEFINITION

        self._linear_solver = 'FGMRES'
        self._linear_solver_prec = 'ILU'
        self._linear_solver_prec_opts = \
            {
                'ILU': 'ILU',
                'LU_SGS': 'LU_SGS',
                'LINELET': 'LINELET',
                'JACOBI': 'JACOBI'
             }

        self._linear_solver_ilu_fill_in = 0
        self._linear_solver_error = 1e-06
        # Max number of iterations of the linear solver for the implicit formulation
        self._linear_solver_iter = 10

        # MULTIGRID PARAMETERS

        self._mglevel = 0
        self._mgcycle = 'V_CYCLE'
        self._mgcycle_opts = {
            'V_CYCLE': 'V_CYCLE',
            'W_CYCLE': 'W_CYCLE',
            'FULLMG_CYCLE': 'FULLMG_CYCLE'
        }
        self._mg_pre_smooth = (1, 2, 3, 3)
        self._mg_post_smooth = (0, 0, 0, 0)
        self._mh_correction_smooth = (0, 0, 0, 0)
        self._mg_damp_restriction = 0.75
        self._mg_damp_prolongation = 0.75

        # FLOW NUMERICAL METHOD DEFINITION

        self._conv_num_method_flow = 'ROE'
        # Convective numerical method
        self._conv_num_method_flow_opts = \
            {
                'JST': 'JST',
                'LAX-FRIEDRICH': 'LAX-FRIEDRICH',
                'CUSP': 'CUSP',
                'ROE': 'ROE',
                'AUSM': 'AUSM',
                'HLLC': 'HLLC',
                'TURKEL_PREC': 'TURKEL_PREC',
                'MSW': 'MSW'
            }
        self._low_mach_corr = 'NO'
        self._low_mach_corr_opts = self.yes_no_opts
        self._low_mach_prec = 'NO'
        self._low_mach_prec_opts = self.yes_no_opts
        self._max_roe_turkel_prec = 5.0

        # Entropy fix coefficient (0.0 implies no entropy fixing, 1.0 implies scalar
        # artificial dissipation)
        self._entropy_fix_ceoff = 0.001

        self._time_discre_flow = 'EULER_IMPLICIT'
        self._time_discre_flow_opts = \
            {
                'RUNGE-KUTTA_EXPLICIT': 'RUNGE-KUTTA_EXPLICIT',
                'EULER_IMPLICIT': 'EULER_IMPLICIT',
                'EULER_EXPLICIT': 'EULER_EXPLICIT'

            }
        self._relaxation_factor_flow = 0.95

        # TURBULENT NUMERICAL METHOD DEFINITION

        self._conv_num_method_turb = 'SCALAR_UPWINND'
        self._time_dicre_turb = 'EULER_IMPLICIT'
        self._cfl_reduction_turb = 0.95

        # HEAT NUMERICAL METHOD DEFINITION

        self._thermal_diffusivity = 1.0

        # ADJOINT-FLOW NUMERICAL METHOD DEFINITION

        self._frozen_limiter_dics = 'NO'
        self._frozen_limiter_dics_opts = self.yes_no_opts

        self._frozen_visc_disc = 'NO'
        self._frozen_visc_disc_opts = self.yes_no_opts

        self._inconsistent_disc = 'NO'
        self._inconsistent_disc_opts = self.yes_no_opts

        self.conv_num_method_adjflow = 'JST'
        self.conv_num_method_adjflow_opts = \
            {
                'JST': 'JST',
                'LAX-FRIEDRICH': 'LAX-FRIEDRICH',
                'ROE': 'ROE'
            }

        self._time_discre_adjflow = 'EULER_IMPLICIT'
        self._time_discre_adjflow_opts = \
            {
                'RUNGE-KUTTA_EXPLICIT': 'RUNGE-KUTTA_EXPLICIT',
                'EULER_IMPLICIT': 'EULER_IMPLICIT'
            }
        self._relaxation_factor_adjflow = 1.0
        self._cfl_reduction_adjflow = 0.8
        self._limit_adjflow = 1e6
        self._mg_adjflow = 'YES'
        self._mg_adjflow_opts = self.yes_no_opts

        # ADJOINT-TURBULENT NUMERICAL METHOD DEFINITION

        self._conv_num_memthod_adjturb = 'SCALAR_UPWIND'
        self._discre_adjturb = 'EULER_IMPLICIT'
        self._cfl_reduction_adjturb = 0.01

        # GEOMETRY EVALUATION PARAMETERS

        self._geo_marker = ('airfoil')
        self._geo_description = 'AIRFOIL'
        self._geo_location_stations = (0.0, 0.5, 1.0)
        self._geo_bounds =(1.5, 3.5)

        self._geo_plot_stations = 'NO'
        self._geo_plot_stations_opts = self.yes_no_opts
        self._geo_number_stations = 25
        self._geo_mode = 'FUNCTION'
        self._geo_mode_opts = \
            {
                'FUNCTION': 'FUNCTION',
                'GRADIENT': 'GRADIENT'
            }

        # GRID ADAPTATION STRATEGY

        self._kind_adapt = 'FULL_FLOW'
        self._kind_adapt_opts = {
            'NONE': 'NONE',
            'PERIODIC': 'PERIODIC',
            'FULL': 'FULL',
            'FULL_FLOW': 'FULL_FLOW',
            'GRAD_FLOW': 'GRAD_FLOW',
            'FULL_ADJOINT': 'FULL_ADJOINT',
            'GRAD_ADJOINT': 'GRAD_ADJOINT',
            'GRAD_FLOW_ADJ': 'GRAD_FLOW_ADJ',
            'ROBUST': 'ROBUST',
            'FULL_LINEAR': 'FULL_LINEAR',
            'COMPUTABLE': 'COMPUTABLE',
            'COMPUTABLE_ROBUST': 'COMPUTABLE_ROBUST',
            'REMAINING': 'REMAINING',
            'WAKE': 'WAKE',
            'SMOOTHING': 'SMOOTHING',
            'SUPERSONIC_SHOCK': 'SUPERSONIC_SHOCK'
        }

        self._new_elems = 5
        self._dualvol_power = 0.5

        self._adapt_boundary = 'YES'
        self._adapt_boundary_opts = self.yes_no_opts

        # DESIGN VARIABLE PARAMETERS

        self._dv_kind = 'FDD_SETTING'
        self._dv_kind_opts = \
            {
                'NO_DEFORMATION': 'NO_DEFORMATION',
                'TRANSLATION': 'TRANSLATION',
                'ROTATION': 'ROTATION',
                'SCALE': 'SCALE',
                'FFD_SETTING': 'FFD_SETTING',
                'FFD_NACELLE': 'FFD_NACELLE',
                'FFD_CONTROL_POINT': 'FFD_CONTROL_POINT',
                'FFD_CAMBER': 'FFD_CAMBER',
                'FFD_THICKNESS': 'FFD_THICKNESS',
                'FFD_TWIST': 'FFD_TWIST',
                'FFD_CONTROL_POINT_2D': 'FFD_CONTROL_POINT_2D',
                'FFD_CAMBER_2D': 'FFD_CAMBER_2D',
                'FFD_THICKNESS_2D': 'FFD_THICKNESS_2D',
                'FFD_TWIST_2D': 'FFD_TWIST_2D',
                'HICKS_HENNE': 'HICKS_HENNE',
                'SURFACE_BUMP': 'SURFACE_BUMP'
            }
        # % Parameters of the shape deformation
        # % - NO_DEFORMATION ( 1.0 )
        # % - TRANSLATION ( x_Disp, y_Disp, z_Disp ), as a unit vector
        # % - ROTATION ( x_Orig, y_Orig, z_Orig, x_End, y_End, z_End )
        # % - SCALE ( 1.0 )
        # % - ANGLE_OF_ATTACK ( 1.0 )
        # % - FFD_SETTING ( 1.0 )
        # % - FFD_CONTROL_POINT ( FFD_BoxTag, i_Ind, j_Ind, k_Ind, x_Disp, y_Disp, z_Disp )
        # % - FFD_NACELLE ( FFD_BoxTag, rho_Ind, theta_Ind, phi_Ind, rho_Disp, phi_Disp )
        # % - FFD_GULL ( FFD_BoxTag, j_Ind )
        # % - FFD_ANGLE_OF_ATTACK ( FFD_BoxTag, 1.0 )
        # % - FFD_CAMBER ( FFD_BoxTag, i_Ind, j_Ind )
        # % - FFD_THICKNESS ( FFD_BoxTag, i_Ind, j_Ind )
        # % - FFD_TWIST ( FFD_BoxTag, j_Ind, x_Orig, y_Orig, z_Orig, x_End, y_End, z_End )
        # % - FFD_CONTROL_POINT_2D ( FFD_BoxTag, i_Ind, j_Ind, x_Disp, y_Disp )
        # % - FFD_CAMBER_2D ( FFD_BoxTag, i_Ind )
        # % - FFD_THICKNESS_2D ( FFD_BoxTag, i_Ind )
        # % - FFD_TWIST_2D ( FFD_BoxTag, x_Orig, y_Orig )
        # % - HICKS_HENNE ( Lower Surface (0)/Upper Surface (1)/Only one Surface (2), x_Loc )
        # % - SURFACE_BUMP ( x_Start, x_End, x_Loc )
        self._dv_marker = ('airfoil')
        self._dv_value = 0.01

        # GRID DEFORMATION PARAMETERS

        self._deform_linear_solver = 'FGMRES'
        self._deform_linear_solver_opts = \
            {
                'FGMRES': 'FGMRES',
                'RESTARTED_FGMRES': 'RESTARTED_FGMRES',
                'BCGSTAB': 'BCGSTAB'
            }
        self._deform_linear_solver_perc = 'ILU'
        self._deform_linear_solver_perc_opts = \
            {
                'ILU': 'ILU',
                'LU_SGS': 'LU_SGS',
                'JACOBI': 'JACOBI'
            }
        self._deform_linear_iter = 1000
        self._deform_nonlinear_iter = 1
        self._deform_console_output = 'YES'
        self._deform_console_output_opts = self.yes_no_opts
        self._deform_tol_factor = 1e-6
        self._deform_coeff = 1e6
        self._deform_stiffness_type = 'WALL_DISTANCE'

        self._deform_stiffness_type_opts = \
            {
                'INVERSE_VOLUME': 'INVERSE_VOLUME',
                'WALL_DISTANCE': 'WALL_DISTANCE',
                'CONSTANT_STIFFNESS': 'CONSTANT_STIFFNESS'
            }
        self._deform_limit = 1e6
        self._visualize_deformation = 'NO'
        self._visualize_deformation_opts = self.yes_no_opts

        # FREE-FORM DEFORMATION PARAMETERS

        self._ffd_tolerance = 1e-10
        self._ffd_iterations = 500
        # % FFD box definition: 3D case (FFD_BoxTag, X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3, X4, Y4, Z4,
        # %                              X5, Y5, Z5, X6, Y6, Z6, X7, Y7, Z7, X8, Y8, Z8)
        # %                     2D case (FFD_BoxTag, X1, Y1, 0.0, X2, Y2, 0.0, X3, Y3, 0.0, X4, Y4, 0.0,
        # %                              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self._ffd_definition_2d_pattern = \
            ('FFD_BoxTag', 'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4',
             'X5', 'Y5', 'Z5', 'X6', 'Y6', 'Z6', 'X7', 'Y7', 'Z7', 'X8', 'Y8', 'Z8')
        self._ffd_definition_3d_pattern = \
            ('FFD_BoxTag', 'X1', 'Y1', 0.0, 'X2', 'Y2', 0.0, 'X3', 'Y3', 0.0, 'X4', 'Y4', 0.0,
             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    @property
    def load_path(self):
        return self._load_path

    @load_path.setter
    def load_path(self, new_load_path):
        self._load_path = new_load_path

    @property
    def save_path(self):
        return self._save_path

    @save_path.setter
    def save_path(self, new_save_path):
        self._save_path = new_save_path

    def load_config(self):
        with open(self.load_path, 'r') as cfg_file:
            self.su2_config = cfg_file.read()

    def get_solved_case(self):
        return self.current_case

    def set_solved_case(self, current_case):
        self.current_case = current_case

    @property
    def case_description(self):
        return self._case_description

    @case_description.setter
    def case_description(self, new_case_desc_val):
        self._case_description = new_case_desc_val

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        self._author = new_author

    @property
    def institution(self):
        return self._institution

    @institution.setter
    def institution(self, new_instit_val):
        self._institution = new_instit_val

    @property
    def cfg_date(self):
        return self._cfg_date

    @cfg_date.setter
    def cfg_date(self, new_date_val):
        self._cfg_date = new_date_val

    # PHYSICAL_PROBLEM
    @property
    def physical_problem(self):
        return self._physical_problem

    @physical_problem.setter
    def physical_problem(self, new_physical_problem_val):
        allowed_problems = (
            'EULER',
            'NAVIER_STOKES',
            'WAVE_EQUATION',
            'HEAT_EQUATION',
            'FEM_ELASTICITY',
            'POISSON_EQUATION')

        self._physical_problem = \
            self._check_and_get_new_val(
                new_physical_problem_val, allowed_problems)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, new_units_val):
        allowed_vals = ('SI', 'US')

        self._units = self._check_and_get_new_val(new_units_val, allowed_vals)

    # REGIME_TYPE
    @property
    def regime_type(self):
        return self._regime_type

    @regime_type.setter
    def regime_type(self, new_regime_type_value):
        allowed_vals = ('COMPRESSIBLE', 'INCOMPRESSIBLE')

        self._regime_type = \
            self._check_and_get_new_val(new_regime_type_value, allowed_vals)

    def _check_and_get_new_val(
            self, new_value, allowed_vals,
            error_message='Some sort of error in combo box - check '
                          'config_editor_widget'):
        if new_value not in allowed_vals:
            raise ValueError(error_message)
        else:
            return new_value

    # compressible free-stream def
    @property
    def mach_number(self):
        return self._mach_number

    @mach_number.setter
    def mach_number(self, new_value):
        self._mach_number = new_value

    @property
    def aoa(self):
        return self._aoa

    @aoa.setter
    def aoa(self, new_value):
        self._aoa = new_value

    @property
    def sideslip(self):
        return self._sideslip

    @sideslip.setter
    def sideslip(self, new_value):
        self._sideslip = new_value

    @property
    def init_option(self):
        return self._init_option

    @init_option.setter
    def init_option(self, new_value):
        self._init_option = new_value

    @property
    def freestream_option(self):
        return self._freestream_option

    @freestream_option.setter
    def freestream_option(self, new_value):
        self._freestream_option = new_value

    @property
    def freestream_pressure(self):
        return self._freestream_pressure

    @freestream_pressure.setter
    def freestream_pressure(self, new_value):
        self._freestream_pressure = new_value

    @property
    def freestream_temperature(self):
        return self._freestream_temperature

    @freestream_temperature.setter
    def freestream_temperature(self, new_value):
        self._freestream_temperature = new_value

    @property
    def reynolds_number(self):
        return self._reynolds_number

    @reynolds_number.setter
    def reynolds_number(self, new_value):
        self._reynolds_number = new_value

    @property
    def renolds_length(self):
        return self._reynolds_length

    @renolds_length.setter
    def renolds_length(self, new_value):
        self._reynolds_length = new_value

    @property
    def freestream_density(self):
        return self._freestream_density

    @freestream_density.setter
    def freestream_density(self, new_value):
        self._freestream_density = new_value

    @property
    def freestream_velocity(self):
        return self._freestream_velociity

    @freestream_velocity.setter
    def freestream_velocity(self, new_value_tuple):
        self._freestream_velociity = new_value_tuple

    @property
    def freestream_viscosity(self):
        return self._freestream_viscosity

    @freestream_viscosity.setter
    def freestream_viscosity(self, new_value):
        self._freestream_viscosity = new_value

    @property
    def fixed_cl_mode(self):
        return self._fixed_cl_mode

    @fixed_cl_mode.setter
    def fixed_cl_mode(self, new_value):
        self._fixed_cl_mode = new_value

    @property
    def target_cl(self):
        return self._target_cl

    @target_cl.setter
    def target_cl(self, new_value):
        self._target_cl = new_value

    @property
    def dcl_alpha(self):
        return self._dcl_alpha

    @dcl_alpha.setter
    def dcl_alpha(self, new_value):
        self._dcl_alpha = new_value

    @property
    def update_alpha(self):
        return self._update_alpha

    @update_alpha.setter
    def update_alpha(self, new_value):
        self._update_alpha = new_value

    @property
    def iter_dcl_alpha(self):
        return self._iter_dcl_alpha

    @iter_dcl_alpha.setter
    def iter_dcl_alpha(self, new_value):
        self._iter_dcl_alpha = new_value
