import json
import math
import logging
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class WireframeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wireframe to Saber Converter")
        self.root.geometry("600x750")
        self.root.minsize(600, 750) # Prevent resizing below the base window size, before the elements were easily cutoff when resized

        # Variables to store user inputs
        self.infile_path = tk.StringVar()
        self.outfile_path = tk.StringVar()
        self.indentation = tk.BooleanVar()
        self.x_rotation = tk.DoubleVar(value=0.0)
        self.y_rotation = tk.DoubleVar(value=0.0)
        self.z_rotation = tk.DoubleVar(value=0.0)
        self.scale = tk.DoubleVar(value=1.0)
        self.x_offset = tk.DoubleVar(value=0.0)
        self.y_offset = tk.DoubleVar(value=0.0)
        self.z_offset = tk.DoubleVar(value=0.0)
        self.r_color = tk.DoubleVar(value=1.0)
        self.g_color = tk.DoubleVar(value=1.0)
        self.b_color = tk.DoubleVar(value=1.0)
        self.a_color = tk.DoubleVar(value=1.0)
        self.edge_width = tk.DoubleVar(value=2.0)  # New width variable

        self.create_widgets()

    def create_widgets(self):
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File selection section
        file_frame = ttk.LabelFrame(
            main_frame, text="File Selection", padding=10
        )
        file_frame.pack(fill=tk.X, pady=(0, 10))

        # Input file
        ttk.Label(file_frame, text="Input .obj file:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(file_frame, textvariable=self.infile_path, width=50).grid(
            row=0, column=1, padx=(5, 5), pady=2
        )
        ttk.Button(file_frame, text="Browse",
                   command=self.browse_input_file).grid(
            row=0, column=2, pady=2
        )

        # Output file
        ttk.Label(file_frame, text="Output file:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(file_frame, textvariable=self.outfile_path, width=50).grid(
            row=1, column=1, padx=(5, 5), pady=2
        )
        ttk.Button(file_frame, text="Browse",
                   command=self.browse_output_file).grid(
            row=1, column=2, pady=2
        )

        # Indentation checkbox
        ttk.Checkbutton(
            file_frame, text="Add indentation to output JSON",
            variable=self.indentation
        ).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Rotation section
        rotation_frame = ttk.LabelFrame(
            main_frame, text="Rotation (degrees)", padding=10
        )
        rotation_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(rotation_frame, text="X Rotation:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(rotation_frame, textvariable=self.x_rotation,
                  width=15).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(rotation_frame, text="Y Rotation:").grid(
            row=0, column=2, sticky=tk.W, pady=2, padx=(20, 0)
        )
        ttk.Entry(rotation_frame, textvariable=self.y_rotation,
                  width=15).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(rotation_frame, text="Z Rotation:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(rotation_frame, textvariable=self.z_rotation,
                  width=15).grid(row=1, column=1, padx=5, pady=2)

        # Scale and offset section
        transform_frame = ttk.LabelFrame(
            main_frame, text="Scale and Offset", padding=10
        )
        transform_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(transform_frame, text="Scale:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(transform_frame, textvariable=self.scale,
                  width=15).grid(row=0, column=1, padx=5, pady=2)

        # Edge width field
        ttk.Label(transform_frame, text="Edge Width:").grid(
            row=0, column=2, sticky=tk.W, pady=2, padx=(20, 0)
        )
        ttk.Entry(transform_frame, textvariable=self.edge_width,
                  width=15).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(transform_frame, text="X Offset:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(transform_frame, textvariable=self.x_offset,
                  width=15).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(transform_frame, text="Y Offset:").grid(
            row=1, column=2, sticky=tk.W, pady=2, padx=(20, 0)
        )
        ttk.Entry(transform_frame, textvariable=self.y_offset,
                  width=15).grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(transform_frame, text="Z Offset:").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(transform_frame, textvariable=self.z_offset,
                  width=15).grid(row=2, column=1, padx=5, pady=2)

        # Color section
        color_frame = ttk.LabelFrame(
            main_frame, text="Color (RGBA values 0.0-1.0)", padding=10
        )
        color_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(color_frame, text="Red:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(color_frame, textvariable=self.r_color,
                  width=15).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(color_frame, text="Green:").grid(
            row=0, column=2, sticky=tk.W, pady=2, padx=(20, 0)
        )
        ttk.Entry(color_frame, textvariable=self.g_color,
                  width=15).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(color_frame, text="Blue:").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        ttk.Entry(color_frame, textvariable=self.b_color,
                  width=15).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(color_frame, text="Alpha:").grid(
            row=1, column=2, sticky=tk.W, pady=2, padx=(20, 0)
        )
        ttk.Entry(color_frame, textvariable=self.a_color,
                  width=15).grid(row=1, column=3, padx=5, pady=2)

        # Process button
        process_frame = ttk.Frame(main_frame)
        process_frame.pack(fill=tk.X, pady=20)

        ttk.Button(
            process_frame, text="Convert Wireframe",
            command=self.process_wireframe, style='Accent.TButton'
        ).pack(pady=10)

        # Status label
        self.status_label = ttk.Label(
            process_frame, text="Ready to convert", foreground="green"
        )
        self.status_label.pack()

    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select .obj input file",
            filetypes=[("OBJ files", "*.obj"), ("All files", "*.*")]
        )
        if filename:
            self.infile_path.set(filename)

    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save output file as",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.outfile_path.set(filename)

    def validate_inputs(self):
        if not self.infile_path.get():
            messagebox.showerror("Error", "Please select an input .obj file")
            return False

        if not self.infile_path.get().endswith('.obj'):
            messagebox.showerror("Error", "Input file must be a .obj file")
            return False

        if not self.outfile_path.get():
            messagebox.showerror("Error", "Please specify an output file path")
            return False

        # Validate color values are between 0 and 1
        color_values = [
            self.r_color.get(), self.g_color.get(),
            self.b_color.get(), self.a_color.get()
        ]
        if any(c < 0 or c > 1 for c in color_values):
            messagebox.showerror(
                "Error", "Color values must be between 0.0 and 1.0"
            )
            return False

        # Validate edge width is positive
        if self.edge_width.get() <= 0:
            messagebox.showerror(
                "Error", "Edge width must be greater than 0"
            )
            return False

        return True

    def process_wireframe(self):
        if not self.validate_inputs():
            return

        try:
            self.status_label.config(
                text="Processing...", foreground="orange"
            )
            self.root.update()

            # Call the main processing function with GUI values
            module_count = self.run_conversion()

            self.status_label.config(
                text=f"Conversion completed! Generated {module_count} modules", 
                foreground="green"
            )
            messagebox.showinfo(
                "Success", 
                f"Wireframe conversion completed successfully!\n"
                f"Generated {module_count} saber modules."
            )

        except Exception as e:
            self.status_label.config(
                text="Error occurred", foreground="red"
            )
            messagebox.showerror(
                "Error", f"An error occurred during conversion:\n{str(e)}"
            )

    def run_conversion(self):
        # This is your main() function logic, adapted for GUI
        modules = []
        vertices = []
        edges = set()

        # Read the .obj file
        with open(self.infile_path.get(), 'r') as f:
            for line in f:
                if line[0] == 'v' and line[1] not in {'t', 'n'}:
                    coordinate = [
                        float(coord) for coord in line.strip().split()[1:]
                    ]
                    if len(coordinate) == 3:
                        vertices.append(coordinate[:3])
                    elif len(coordinate) == 6:
                        vertices.append(coordinate[3:])

                if line[0] == 'f':
                    vertex_indices = [
                        int(part.split('/')[0]) - 1
                        for part in line.strip().split()[1:]
                    ]
                    for i in range(len(vertex_indices)):
                        a = vertex_indices[i]
                        b = vertex_indices[(i + 1) % len(vertex_indices)]

                        if a == b:
                            continue

                        edges.add(tuple(sorted((a, b))))

        # Apply rotations
        if self.x_rotation.get():
            vertices = [
                rotate_point_around_axis(
                    vertice, [1, 0, 0], self.x_rotation.get()
                )
                for vertice in vertices
            ]

        if self.y_rotation.get():
            vertices = [
                rotate_point_around_axis(
                    vertice, [0, 1, 0], self.y_rotation.get()
                )
                for vertice in vertices
            ]

        if self.z_rotation.get():
            vertices = [
                rotate_point_around_axis(
                    vertice, [0, 0, 1], self.z_rotation.get()
                )
                for vertice in vertices
            ]

        # Apply scaling
        if self.scale.get() != 1:
            vertices = [
                tuple(coord) for coord in np.array(vertices) * self.scale.get()
            ]

        # Apply offset
        vertices = add_offset(vertices, 0, self.x_offset.get())
        vertices = add_offset(vertices, 1, self.y_offset.get())
        vertices = add_offset(vertices, 2, self.z_offset.get())

        # Generate edges
        rgba = (
            self.r_color.get(), self.g_color.get(),
            self.b_color.get(), self.a_color.get()
        )

        for edge in sorted(edges):
            blade_mappings = {
                "colorOverValue": {
                    "interpolationType": 0,
                    "controlPoints": [
                        {
                            "time": 0.0,
                            "value": add_axes(rgba, ['r', 'g', 'b', 'a'])
                        }
                    ]
                },
                "alphaOverValue": {
                    "interpolationType": 0,
                    "controlPoints": [
                        {
                            "time": 0.0,
                            "value": 1.0
                        }
                    ]
                },
                "scaleOverValue": {
                    "interpolationType": 0,
                    "controlPoints": [
                        {
                            "time": 0.0,
                            "value": 1.0
                        }
                    ]
                },
                "valueFrom": 0.0,
                "valueTo": 1.0
            }

            if any(vertex > len(vertices) for vertex in edge):
                break

            modules = generate_edge(
                modules, vertices[edge[0]], vertices[edge[1]],
                width=self.edge_width.get(),
                blade_mappings=blade_mappings
            )

        print(f'Saber is {len(modules)} modules')
        reesaber_export(
            modules, self.outfile_path.get(),
            no_indent=not self.indentation.get()
        )
        
        return len(modules)  # Return module count


# Your existing functions (unchanged)
def get_3d_distance(coordinate1, coordinate2):
    return np.linalg.norm(np.array(coordinate1) - np.array(coordinate2))


def get_middle(coordinate1, coordinate2):
    return [
        (coord1 + coord2) / 2
        for coord1, coord2
        in zip(coordinate1, coordinate2)
    ]


def generate_edge(
    modules, coordinate1, coordinate2, width=10.0,
    blade_mappings={
        "colorOverValue": {
            "interpolationType": 0,
            "controlPoints": [
                {
                    "time": 0.0,
                    "value": {
                        "r": 1.0,
                        "g": 0.12,
                        "b": 0.0,
                        "a": 0.0
                    }
                }
            ]
        },
        "alphaOverValue": {
            "interpolationType": 0,
            "controlPoints": [
                {
                    "time": 0.0,
                    "value": 1.0
                }
            ]
        },
        "scaleOverValue": {
            "interpolationType": 0,
            "controlPoints": [
                {
                    "time": 0.0,
                    "value": 1.0
                }
            ]
        },
        "valueFrom": 0.0,
        "valueTo": 1.0
    },
):
    length = get_3d_distance(coordinate1, coordinate2)
    middle = get_middle(coordinate1, coordinate2)
    x_rot, y_rot = get_zxy_rotation(coordinate1, coordinate2)

    if not x_rot and not y_rot:
        return modules

    return reesaber_create_blur_saber(
        modules, name=f'edge_{middle}', z_offset_from=(length / -2),
        z_offset_to=(length / 2), saber_thickness=width/22.4,
        vertical_resolution=2, horizontal_resolution=1,
        blade_mappings=blade_mappings,
        local_transform={
            "Position": add_axes(middle),
            "Rotation": {
                "x": x_rot,
                "y": y_rot,
                "z": 0.0
            },
            "Scale": {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0
            }
        },
        handle_mask={
            "interpolationType": 2,
            "controlPoints":
            [
                {
                    "time": 0.0,
                    "value": 0.0
                }
            ]
        },
    )


def add_axes(add_to, labels=['x', 'y', 'z']):
    return {
        axis: coord for axis, coord in zip(labels, add_to)
    }


def get_zxy_rotation(coordinate1, coordinate2):
    dx = coordinate2[0] - coordinate1[0]
    dy = coordinate2[1] - coordinate1[1]
    dz = coordinate2[2] - coordinate1[2]

    length = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    if length == 0:
        return None, None

    dx /= length
    dy /= length
    dz /= length

    x_rot = -math.degrees(math.atan2(dy, math.sqrt(dx ** 2 + dz ** 2)))
    y_rot = math.degrees(math.atan2(dx, dz))

    return x_rot, y_rot


def rotate_point_around_axis(point, axis, angle_deg):
    angle_rad = np.radians(angle_deg)
    axis = np.array(axis)
    axis = axis / np.linalg.norm(axis)

    point = np.array(point)

    cos_theta = np.cos(angle_rad)
    sin_theta = np.sin(angle_rad)
    cross = np.cross(axis, point)
    dot = np.dot(axis, point)
    rotated = (
        point * cos_theta +
        cross * sin_theta +
        axis * dot * (1 - cos_theta)
    )

    return rotated.tolist()


def add_offset(coordinates, which, how_much):
    array = np.array(coordinates)
    array[:, which] += how_much
    return array


def configLog(level=logging.INFO, filename="ReeSaber Python.log"):
    logging.basicConfig(filename=filename, level=level,
                        format='%(asctime)s - [%(levelname)s] - %(message)s')


def reesaber_create_blur_saber(
    modules, name="Blur Saber", scale_factor=1.0, z_offset_from=-0.17,
    z_offset_to=1.0, saber_thickness=1.0, start_cap=True, end_cap=True,
    vertical_resolution=20, horizontal_resolution=10, blur_frames=2.0,
    glow_multiplier=1.0, handle_roughness=2.0, handle_color=None,
    blade_mask_resolution=256, drivers_mask_resolution=32, cull_mode=0,
    depth_write=False, render_queue=3002, handle_mask=None,
    blade_mappings=None, drivers_sample_mode=0, viewing_angle_mappings=None,
    surface_angle_mappings=None, local_transform=None, saber_profile=None,
    drivers=[]
):
    if handle_color is None:
        handle_color = {
            "r": 0.1,
            "g": 0.1,
            "b": 0.1,
            "a": 0.0
        }

    if handle_mask is None:
        handle_mask = {
            "interpolationType": 2,
            "controlPoints":
            [
                {
                    "time": 0.0,
                    "value": 0.0
                },
                {
                    "time": 0.028,
                    "value": 1.0
                },
                {
                    "time": 0.128,
                    "value": 0.0
                },
                {
                    "time": 0.145,
                    "value": 1.0
                },
                {
                    "time": 0.17,
                    "value": 0.0
                }
            ]
        }

    if blade_mappings is None:
        blade_mappings = {
            "colorOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": {
                            "r": 1.0,
                            "g": 1.0,
                            "b": 1.0,
                            "a": 1.0
                        }
                    }
                ]
            },
            "alphaOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": 1.0
                    }
                ]
            },
            "scaleOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": 1.0
                    }
                ]
            },
            "valueFrom": 0.0,
            "valueTo": 1.0
        }

    if viewing_angle_mappings is None:
        viewing_angle_mappings = {
            "colorOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": {
                            "r": 1.0,
                            "g": 1.0,
                            "b": 1.0,
                            "a": 1.0
                        }
                    }
                ]
            },
            "alphaOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": 1.0
                    }
                ]
            },
            "scaleOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": 1.0
                    }
                ]
            },
            "valueFrom": 0.0,
            "valueTo": 1.0
        }

    if surface_angle_mappings is None:
        surface_angle_mappings = {
            "colorOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": {
                            "r": 1.0,
                            "g": 1.0,
                            "b": 1.0,
                            "a": 1.0
                        }
                    }
                ]
            },
            "alphaOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": 1.0
                    }
                ]
            },
            "scaleOverValue": {
                "interpolationType": 0,
                "controlPoints": [
                    {
                        "time": 0.0,
                        "value": 1.0
                    }
                ]
            },
            "valueFrom": 0.0,
            "valueTo": 1.0
        }

    if local_transform is None:
        local_transform = {
            "Position": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "Rotation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "Scale": {
                "x": scale_factor,
                "y": scale_factor,
                "z": scale_factor
            }
        }

    if saber_profile is None:
        saber_profile = {
            "interpolationType": 1,
            "controlPoints": [
                {
                    "time": 0.0,
                    "value": 1.0
                },
                {
                    "time": 1.0,
                    "value": 1.0
                }
            ]
        }

    modules.append({
        "ModuleId": "reezonate.blur-saber",
        "Version": 1,
        "Config": {
            "SaberSettings": {
                "zOffsetFrom": z_offset_from,
                "zOffsetTo": z_offset_to,
                "thickness": saber_thickness,
                "saberProfile": saber_profile,
                "startCap": start_cap,
                "endCap": end_cap,
                "verticalResolution": vertical_resolution,
                "horizontalResolution": horizontal_resolution,
                "renderQueue": render_queue,
                "cullMode": cull_mode,
                "depthWrite": depth_write,
                "blurFrames": blur_frames,
                "glowMultiplier": glow_multiplier,
                "handleRoughness": handle_roughness,
                "handleColor": handle_color,
                "maskSettings": {
                    "bladeMaskResolution": blade_mask_resolution,
                    "driversMaskResolution": drivers_mask_resolution,
                    "handleMask": handle_mask,
                    "bladeMappings": blade_mappings,
                    "driversSampleMode": drivers_sample_mode,
                    "viewingAngleMappings": viewing_angle_mappings,
                    "surfaceAngleMappings": surface_angle_mappings,
                    "drivers": drivers
                }
            },
            "Enabled": True,
            "Name": name,
            "LocalTransform": local_transform
        }
    })
    return modules


def reesaber_export(modules, save_to, no_indent=False):
    saber_json = {
        "ModVersion": "0.3.9",
        "Version": 1,
        "LocalTransform": {
            "Position": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "Rotation": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "Scale": {
                "x": 1.0,
                "y": 1.0,
                "z": 1.0
            }
        },
        "Modules": modules
    }

    try:
        with open(save_to, "w") as f:
            f.write(json.dumps(saber_json, indent=None if no_indent else 4))
    except Exception as e:
        logging.error(f"export(): {e}")


def main():
    root = tk.Tk()
    app = WireframeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
